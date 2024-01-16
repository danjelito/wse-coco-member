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
    memberships = np.select(conditions, choices, default="Not Specified")

    return memberships


def get_cpt(df_: pd.DataFrame) -> pd.Series:
    """
    Determine whether a student is a CPT student or not
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
    # member have corporate consultant
    consultant_cpt = df_["consultant"].str.upper().isin(cpt_consultants)
    # member have CPT identifier in their name
    id_contains_cpt = (
        df_["student_code"].str.lower().str.contains(r"\Wcpt\W", regex=True, na=False)
    )
    is_cpt = consultant_cpt | id_contains_cpt
    return is_cpt


def get_member_center_from_consultant(consultant: pd.Series) -> pd.Series:
    """
    Get member center from their consultant's center.
    Useful for members who does not have center identifier.

    :param pd.Series consultant: Consultant of that member.
    :return pd.Series: The consultant's center.
    """

    map_consultant = {
        "SalawATI (PP) NATALIA JOPHINA": "PP",
        "YAN FIRSUS TUMANGGOR (KK) SAMUEL": "KK",
        "(DG) ABIMANYU ABDUL KARIM": "DG",
        "RAVEN RIZQULLAH (CBB) MUHAMMAD": "CBB",
        "TOMBOKAN NATANIA ATHENA": "PP",
        "(DG) SALSHABILA SUDRAJAT ALTIARA ASRA": "DG",
        "ABDULBAR SOEDIBYO (BSD)FADHIEL": "BSD",
        "YOLANDHA (LW) NADYA PUSPA": "LW",
        "LELITYA (SDC) ZARAH": "SDC",
        "PRATIWI (KK) AZZAHRA NADIA": "KK",
        "(DG) LAVINDI CLARISA TANTIOLA": "DG",
        "BAYU SYAHPUTRO (SDC) MUHAMMAD": "SDC",
        "(DG) HUTASOIT ESTHER SETIAWATI": "DG",
        "RAHMA (KK) JIHAN BALQIS FITRIA": "KK",
        "ROMAINUR (KK) SILVIA OLYVERA": "KK",
        "WINARDO (KK) ABRI": "KK",
        "ADIESTI (PP) DENNISSA AULIA": "PP",
        "FRANSISCA LUBIS (KK) DIANA SUSAN": "KK",
        "ESTUNINGTYAS (PP) MENIK": "PP",
        "MICHELLE (GC) FEMME": "GC",
        "THEODORUS (PP) KEVIN JOSHUA": "PP",
        ". (GC) YUNINGSIH": "GC",
        "ZAELANI (PP) MUHAMMAD SOLEH": "PP",
        "WIBOWO (GC) ROBI": "GC",
        "FITRIA RAHMA JIHAN BALQIS": "KK",
        "SHIDIQ NUGRAHA MUHAMAD IQBAL": "GC",
        "TAMBUN YOHANIS": "SDC",
        "FAJRIA SAHISTA ACHADIARROHMA": "PKW",
        "PERMANA SAKA": "GC",
        "OKTARIA BR GINTING GRACETY FANI": "PP",
        "AULIA LUBIS DEA DEFANNI": "PP",
        "HAMIDIYATI NAZIFA": "GC",
        "CHRISTIAN CLIVEN": "PP",
        "NATHANIEL MICHAEL": "PP",
        "PRATIWI PUSPA": "PKW",
        "AZIZ MALDI ABDUL": "GC",
        "JAGANEGARA HAIDAR": "GC",
        "AKHMAL AMMAARZA": "KK",
        "CHANDRA CHANDRA": "PP",
        "MASITA MAYANG DEA": "PKW",
        "KHAERUNNISA QURRATU AIN": "CBB",
        "SEKAR AYU ADINDA ATHARIKA": "KK",
        "PRIHASTIWI NURALISTA": "CBB",
        "MONETRI FEBI CATUR": "GC",
        "APSARI KEISA CHAIRANI": "PKW",
        "SALSHABILA SUDRAJAT ALTIARA ASRA": "DG",
        "AULIA HASNA": "DG",
        "YOLANDHA NADYA": "LW",
        "SANUSI SOFIA NUR INDAH EKATAMI": "KK",
        "ANGGA ERON": "KK",
        "RAVEN RIZQULLAH MUHAMMAD": "CBB",
        "ROSADI IMRON": "KK",
    }
    return consultant.map(map_consultant, na_action=None)


def get_center(df_: pd.DataFrame) -> pd.Series:
    """
    Determine the center of the student
    based on the marker inside the name (for example DLC GC).
    If the member does not have marker then use function get_member_center_from_consultant
    to get center from consultant.

    :param pd.DataFrame df_: Dataframe.
    :return pd.Series: Center of each student. If no match the np.nan.
    """

    pattern = f'({"|".join(centers)})'

    conditions = [
        # corporate
        (df_["is_cpt"] == True),
        # online center
        (df_["student_membership"].str.lower() == "go"),
        # member code does not contain center identifier
        ~(df_["student_code"].str.upper().str.contains(pattern, regex=True, na=False)),
        # deluxe and vip, assuming they have center identifier
        (df_["student_membership"].str.lower().isin(["deluxe", "vip"])),
    ]

    choices = [
        "Corporate",
        "Online Center",
        (get_member_center_from_consultant(df_["consultant"].str.upper())),
        (
            df_["student_code"]
            .str.extract("(\(.+\))", expand=False)
            .str.replace("(", "", regex=False)
            .str.replace(")", "", regex=False)
            .str.extract(pattern, expand=False)
        ),
    ]

    student_center = np.select(conditions, choices, default="Not Specified")
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
    area = np.select(conditions, choices, default="Not Specified")
    assert (area == "ERROR").sum() == 0, "Some centers are unmapped to area"
    return area


def clean_phone_number(ser: pd.Series) -> pd.Series:
    """Clean the phone number.

    :param pd.Series ser: phone number.
    :return pd.Series: cleaned phone number.
    """
    return (
        ser
        .astype(str)
        .str.replace("-", "", regex=False)
        .str.replace("+", "", regex=False)
        .str.strip()
    )
