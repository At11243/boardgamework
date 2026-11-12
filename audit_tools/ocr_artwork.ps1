param([Parameter(Mandatory=$true)][string]$Jobs)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Runtime.WindowsRuntime
[Windows.Storage.StorageFile, Windows.Storage, ContentType=WindowsRuntime] | Out-Null
[Windows.Storage.Streams.IRandomAccessStream, Windows.Storage.Streams, ContentType=WindowsRuntime] | Out-Null
[Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType=WindowsRuntime] | Out-Null
[Windows.Graphics.Imaging.SoftwareBitmap, Windows.Graphics.Imaging, ContentType=WindowsRuntime] | Out-Null
[Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType=WindowsRuntime] | Out-Null
[Windows.Media.Ocr.OcrResult, Windows.Foundation, ContentType=WindowsRuntime] | Out-Null
$taskMethod=[System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.IsGenericMethod -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' } | Select-Object -First 1
function Await-Result($operation,$resultType) {
 $task=$taskMethod.MakeGenericMethod($resultType).Invoke($null,@($operation));$task.Wait();return $task.Result
}
$engine=[Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
if ($null -eq $engine) {throw 'Windows OCR language unavailable'}
$count=0
foreach ($job in (Get-Content -LiteralPath $Jobs -Raw | ConvertFrom-Json)) {
 if (Test-Path -LiteralPath $job.output) {continue}
 $file=Await-Result ([Windows.Storage.StorageFile]::GetFileFromPathAsync($job.image)) ([Windows.Storage.StorageFile])
 $stream=Await-Result ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
 $decoder=Await-Result ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
 $bitmap=Await-Result ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
 $result=Await-Result ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
 $words=@(foreach($line in $result.Lines){foreach($word in $line.Words){@{text=$word.Text;x=$word.BoundingRect.X;y=$word.BoundingRect.Y;w=$word.BoundingRect.Width;h=$word.BoundingRect.Height}}})
 @{text=$result.Text;words=$words;source_image=$job.image;engine='Windows.Media.Ocr'} | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $job.output -Encoding UTF8
 $bitmap.Dispose();$stream.Dispose();$count++
 if ($count % 20 -eq 0) {Write-Output "OCR panels completed: $count"}
}
Write-Output "Finished $count new panels"
