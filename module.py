import pandas as pd
import numpy as np


def create_student_membership(df: pd.DataFrame):
    """
        Create series marking student membership type.
        Standard Deluxe can join online and offline class.
        Standard GO can only join online class.
        # note: as per 2023-02-08, CAD has put (GO) in all GO members, making it possible to separate GO.

    Args:
        df (pd.DataFrame)

    Returns:
        memberships
    """

    membership_contains_std = df["service_type"] == "Standard"
    membership_contains_vip = df["service_type"] == "VIP"
    name_contains_dlx = (
        df["student_code"].str.upper().str.contains("(DLX", regex=False, na=False)
    )
    name_contains_go = (
        df["student_code"].str.upper().str.contains("(GO", regex=False, na=False)
    )
    mask_deluxe_1 = (~name_contains_go) & membership_contains_std
    mask_deluxe_2 = (~name_contains_go) & name_contains_dlx

    conditions = [
        name_contains_go,
        mask_deluxe_1,
        mask_deluxe_2,
        membership_contains_vip,
    ]
    choices = ["GO", "Deluxe", "Deluxe", "VIP"]
    memberships = np.select(conditions, choices, default="Error")

    return memberships
