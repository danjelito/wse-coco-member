import pandas as pd
import numpy as np
import config


def load_multiple_dfs(df_list: list) -> pd.DataFrame:
    """Load all DF listed in the df_list and return them as one DF.

    :param list df_list: paths of DFs.
    :return pd.DataFrame: concatted DF.
    """
    dfs = []
    for filepath in df_list:
        df = pd.read_excel(filepath, skiprows=6)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)


def create_student_code(df_: pd.DataFrame) -> pd.Series:
    """
    Create new student code from last name, first name and code
    Like last_name first_name code.

    :param pd.DataFrame df_: DF to process.
    :return pd.Series: Student code.
    """
    return (
        df_["last_name"].str.upper()
        + " "
        + df_["first_name"].str.upper()
        + " - "
        + df_["student_code"].astype("str")
    ).str.strip()


def create_student_membership(df_: pd.DataFrame) -> pd.Series:
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

    membership_contains_std = df_["service_type"] == "Standard"
    membership_contains_vip = df_["service_type"] == "VIP"
    name_contains_dlx = (
        df_["student_code"].str.upper().str.contains("(DLX", regex=False, na=False)
    )
    name_contains_go = (
        df_["student_code"].str.upper().str.contains("(GO", regex=False, na=False)
    )
    mask_deluxe_1 = (~name_contains_go) & membership_contains_std
    mask_deluxe_2 = (~name_contains_go) & name_contains_dlx

    conditions = [
        name_contains_go,
        mask_deluxe_1,
        mask_deluxe_2,
        membership_contains_vip,
    ]
    choices = ["Go", "Deluxe", "Deluxe", "VIP"]
    memberships = np.select(conditions, choices, default="NONE")

    # assert that all memberships are specified
    assert not (memberships == "NONE").sum()

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
    ! NEED TO DEBUG WHY SOME ARE NOT MAPPED
    Get member center from their consultant's center.
    Useful for members who does not have center identifier.

    :param pd.Series consultant: Consultant of that member.
    :return pd.Series: The consultant's center.
    """

    map_consultant = {
        "SALAWATI (PP) NATALIA JOPHINA": "PP",
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
        # new ""
        "SUNARTO (BSD) EUPHEMIA ERNEST": "BSD",
        "SUBANDI (PKW) WILLIAM HERDIYANTO": "PKW",
        "(DG) HUTASOIT ESTHER SETIAWATI": "DG",
        "NUGROHO (LW) YOHANES ADHI": "LW",
        "VISCA (GC) NATHASYA MONICA": "GC",
        "LESMANA PUTRI (GC) CHANELEEN MARVEL": "GC",
        "(DG) PURBA RAPHAEL ZEFANYA": "DG",
        "PATRIASARI (SDC) RUTH EMY": "SDC",
        "KHOIRURRIZKY (PKW)FIRDA": "PKW",
        "JABRY (GC) FAIS AL": "GC",
        "AMANI (LW) SUHA": "LW",
        "IBRAHIM (PP) FAISAL MAULANA": "PP",
        "RAMADHAN (CBB) ALDI": "CBB",
        "(DG) SALSHABILA SUDRAJAT ALTIARA ASRA": "DG",
        "IDAYATI (PKW) DILLA": "PKW",
        "AREZANTI (PP) SOPHIA DEWI": "PP",
        "HIDAYAT (LW) DIMAS DARMAWAN SUSILO": "LW",
        "THEODORUS (PP) KEVIN JOSHUA": "PP",
        "PRATIWI (BSD) SITI CHOIRIYAH": "BSD",
        "VIRGIANO (PKW) MAXELL": "PKW",
        "BAYU SYAHPUTRO (SDC) MUHAMMAD": "SDC",
        "WINARDO (KK) ABRI": "KK",
        "ROMAINUR (KK) SILVIA OLYVERA": "KK",
        "(DG) ABIMANYU ABDUL KARIM": "DG",
        "NUGROHO RAHARDIAN WAHYU": "SDC",
        "CHUMAIROH RAHMA": "GC",
        "WIJAYA MEVIS VALERIA": "PP",
        "SIREGAR TIURMAIDA": "KK",
        "ANGGRAINI DIAH AYU": "KK",
        "DANEA SINDI DINI": "KK",
        "SIMANJUNTAK YANUAR JOSUA ALBERT MILANO": "PKW",
        "NURYADI DEDE ALI": "KK",
        "SHIDIQ NUGRAHA MUHAMAD IQBAL": "GC",
        "LELITYA ZARAH": "KK",
        "ZAELANI MUHAMMAD SOLEH": "PP",
        "CHANDRA CHANDRA": "PP",
        "PRATIWI PUSPA": "PKW",
        "PUTRI AISYAH JAZULI": "PKW",
        "ESTUNINGTYAS MENIK": "PP",
        "SUNARTO EUPHEMIA ERNEST": "GC",
        "LEE GABRILLE": "SDC",
        "RAMADHAN ALDI": "CBB",
        "EMY PATRIASARI RUTH": "SDC",
        "YUNINGSIH YUNI": "GC",
        "SIAHAAN RUTH ANGGRAINI": "SDC",
        "ADLINNAKA ALNOCHAJASHANY": "CBB",
        "MICHELLE FEMME": "GC",
        "HIDAYAT DIMAS": "LW",
        "NUGROHO YOHANES": "LW",
        "JABRY FAIS AL": "GC",
        "ZEFANYA PURBA RAPHAEL": "DG",
        "SUBANDI WILLIAM HERDIYANTO": "PKW",
        "VISCA NATHASYA": "GC",
        "SYAHPUTRA MUHAMMAD ICHSAN": "GC",
        "KARIM ABDUL": "DG",
        "WSE CAD": "HO",
        "SAABIHAAT DLIYAA US": "KK",
        "PRATIWI AZZAHRA NADIA": "CBB",
        "AREZANTI SOPHIA": "PP",
        "ISMAIL LAKSMI RAMADHITA": "PP",
        "RAMADHAN AUDIA": "DG",
        "PRAMUDYA MUHAMMAD FAREL": "TBS",
        "SATI RIFALDI YUSUF": "TBS"
    }
    return consultant.map(map_consultant, na_action=None)


def get_student_center(df_: pd.DataFrame) -> pd.Series:
    """
    Determine the center of the student
    based on the marker inside the name (for example DLC GC).
    If the member does not have marker then use function get_member_center_from_consultant
    to get center from consultant.

    :param pd.DataFrame df_: Dataframe.
    :return pd.Series: Center of each student. If no match the np.nan.
    """

    pattern = f'({"|".join(config.centers)})'

    conditions = [
        # corporate
        (df_["is_cpt"] == True),
        # online center
        (df_["student_membership"].str.lower() == "go"),
        # ST
        (
            df_["student_code"]
            .str.upper()
            .str.contains("STREET TALK|STREETTALK|\(ST\)", regex=True, na=False)
        ),
        # member code does not contain center identifier
        ~(df_["student_code"].str.upper().str.contains(pattern, regex=True, na=False)),
        # deluxe and vip, assuming they have center identifier
        (df_["student_membership"].str.lower().isin(["deluxe", "vip"])),
    ]

    choices = [
        "Corporate",
        "Online Center",
        "Street Talk",
        (get_member_center_from_consultant(df_["consultant"].str.upper())),
        (df_["student_code"].str.extract(pattern, expand=False)),
    ]

    student_center = np.select(conditions, choices, default="NONE")
    return student_center


def get_area(df_):
    """Determine the area of the student.

    :param pd.DataFrame df_: Dataframe.
    :return pd.Series: Area of each student.
    """
    conditions = [
        df_["student_center"].isna(),
        df_["student_center"].isin(config.map_areas.get("JKT 1")),
        df_["student_center"].isin(config.map_areas.get("JKT 2")),
        df_["student_center"].isin(config.map_areas.get("JKT 3")),
        df_["student_center"].isin(config.map_areas.get("BDG")),
        df_["student_center"].isin(config.map_areas.get("SBY")),
        df_["student_center"].isin(config.map_areas.get("Other")),
        df_["student_center"].isin(config.map_areas.get("Corporate")),
        df_["student_center"].isin(config.map_areas.get("Online Center")),
    ]
    choices = [
        "NONE",
        "JKT 1",
        "JKT 2",
        "JKT 3",
        "BDG",
        "SBY",
        "Other",
        "Corporate",
        "Online Center",
    ]
    area = np.select(conditions, choices, default="NONE")
    return area


def clean_phone_number(ser: pd.Series) -> pd.Series:
    """Clean the phone number.

    :param pd.Series ser: phone number.
    :return pd.Series: cleaned phone number.
    """
    return (
        ser.astype(str)
        .str.replace("-", "", regex=False)
        .str.replace("+", "", regex=False)
        .str.strip()
    )
