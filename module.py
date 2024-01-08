import pandas as pd
import numpy as np

# map centre here
# note: update if there are new centers
jkt_1 = ["PP", "SDC", "KG"]
jkt_2 = ["GC", "LW", "BSD", "TBS"]
jkt_3 = ["KK", "CBB", "SMB"]
bdg = ["DG"]
sby = ["PKW"]
centers = jkt_1 + jkt_2 + jkt_3 + bdg + sby


def create_student_membership(df: pd.DataFrame) -> pd.Series:
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


def get_cpt(df_: pd.DataFrame) -> pd.Series:
    """Determine whether a student is a CPT student or not
    based on consultants and ID.

    :param pd.DataFrame df_: Dataframe.
    :return pd.Series: Boolean.
    """

    cpt_consultants = [
        "PUTRI HANDAYANI KUN ANDIKA",
        "ZULFADLI ZULFADLI",
        "DIREDJA DENNY DARMAWAN",
        "LIMUEL DONNA",
        "AMALIA, S.T RINA",
        "TEDJOKOESOEMO PUTRA PRATAMA",
        "AIDIL MUNAWAR",
        "AMALIA SYIFA",
        "DIREDJA DENNY",
    ]
    consultant_cpt = df_["consultant"].str.upper().isin(cpt_consultants)
    id_contains_cpt = (
        df_["student_code"].str.lower().str.contains(r"\Wcpt\W", regex=True, na=False)
    )
    is_cpt = consultant_cpt | id_contains_cpt
    return is_cpt


def get_center(df_: pd.DataFrame) -> pd.Series:
    """Determine the center of the student
    based on the marker inside the name (for example DLC GC).

    :param pd.DataFrame df_: Dataframe.
    :return pd.Series: Center of each student. If no match the np.nan.
    """

    pattern = f'({"|".join(centers)})'

    conditions = [
        (df_["is_cpt"] == True),
        (df_["student_membership"].str.lower() == "go"),
        (df_["student_membership"].str.lower().isin(["deluxe", "vip"])),
    ]

    choices = [
        "Corporate",
        "Online Center",
        (
            df_["student_code"]
            .str.extract("(\(.+\))", expand=False)
            .str.replace("(", "", regex=False)
            .str.replace(")", "", regex=False)
            .str.extract(pattern, expand=False)
        ),
    ]

    student_center = np.select(conditions, choices, default=np.NaN)
    return student_center

def get_area(df_):
    """Determine the area of the student.

    :param pd.DataFrame df_: Dataframe.
    :return pd.Series: Area of each student. 
    """
    conditions = [
        df_["student_center"].isna(),
        df_["student_center"] == "Corporate",
        df_["student_center"] == "Online Center",
        df_["student_center"].isin(jkt_1),
        df_["student_center"].isin(jkt_2),
        df_["student_center"].isin(jkt_3),
        df_["student_center"].isin(bdg),
        df_["student_center"].isin(sby),
    ]
    choices = [
        np.nan, 
        "Corporate", 
        "Online Center", 
        "JKT 1",
        "JKT 2",
        "JKT 3",
        "BDG",
        "SBY",
    ]
    area = np.select(conditions, choices, default="ERROR")
    assert (area == "ERROR").sum() == 0, "Some centers are unmapped to area"
    return area