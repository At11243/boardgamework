"""Public entry points for independent TSWW rule systems.

Dice follows v1.6a Rule 2.C.1 (printed p8 / PDF p10).
Keep UI and campaign persistence outside this package.
"""
from .dice import DiceService, ROLL_TYPES, DICE_SOURCE, dice_value, roll_dice, validate_roll
from .combat_records import attack_result_record, validate_attack_result

__all__ = [
    "DiceService", "ROLL_TYPES", "DICE_SOURCE", "dice_value", "roll_dice", "validate_roll",
    "attack_result_record", "validate_attack_result",
]
