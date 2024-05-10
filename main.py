import os
from pathlib import Path
import pandas as pd
import config
import module
import tests

# load DF
folder_path = Path("input", config.month)
df_list = [i for i in folder_path.glob("*.xls")]
df_ori = module.load_multiple_dfs(df_list)

# clean DF
df_clean = (df_ori
    .dropna(how="all", axis="columns")
    .dropna(how="all", axis="rows")
    .rename(columns=lambda c: c.lower().replace(" ", "_"))  # replace space with _
    .assign(
        student_name=lambda df_: module.create_student_name(df_),
        student_membership=lambda df_: module.create_student_membership(df_),
        student_code=lambda df_: module.create_student_code(df_),
        start_level=lambda df_: df_["start_level"].astype(float),
        current_level=lambda df_: df_["current_level"].astype(float),
        date_of_birth=lambda df_: pd.to_datetime(df_["date_of_birth"]),
        start_date=lambda df_: pd.to_datetime(df_["start_date"]),
        end_date=lambda df_: pd.to_datetime(df_["end_date"]),
        email=lambda df_: df_["email"].str.lower().str.strip(),
        mobile=lambda df_: module.clean_phone_number(df_["mobile"]),
        consultant = lambda df_: df_["consultant"].str.upper(),
        is_cpt = lambda df_: module.get_cpt(df_), 
        student_center = lambda df_: module.get_student_center(df_),
        student_area = lambda df_: module.get_area(df_),
    )
    .assign(
        student_center = lambda df_: df_["student_center"].fillna("NONE"),
        student_area = lambda df_: df_["student_area"].fillna("NONE"),
    )
    # ! drop ST
    .loc[
        lambda df_: ~(
            df_["student_code"].str.contains("STREET TALK|STREETTALK", na=False)
        )
    ]
    # ! drop duplicated member based on student code, end date and student name
    # somehow there is a student with different start date but same end date
    .drop_duplicates(subset=["student_code", "end_date"], keep="first")
    .drop_duplicates(subset=["student_code", "student_name"], keep="first")
    # ! drop unnecessary cols
    .drop(
        columns=[
            "gender", "home", "work", "end_level", "on_track", "course_status", 
            "personal_tutor", "first_name", "last_name", "center_name",
        ]
    )
)

# for code with multiple name, check the email
# most probably this is due to 1 account being freezed
# or cad sales
# or contract being invalid
for idx, code in module.get_code_with_multiple_name(df_clean, "student_code", "student_name"):

    code_match = df_clean["student_code"] == code
    name_contains_freeze = df_clean["student_name"].str.lower().str.contains("freeze")
    name_contains_cad = df_clean["student_name"].str.lower().str.contains("cad_sales|cad sales")
    contract_invalid = df_clean["contract_status"] == "Invalid"
    
    # if there is only one email
    if df_clean.loc[code_match, "email"].nunique() == 1:
        # drop one name with "freeze"
        idx_duplicate = df_clean.loc[code_match & name_contains_freeze].index.values
        df_clean = df_clean.drop(idx_duplicate, axis="index")
        # drop one name with "cad_sales"
        idx_duplicate = df_clean.loc[code_match & name_contains_cad].index.values
        df_clean = df_clean.drop(idx_duplicate, axis="index")
    
    # if there is multiple email
    else:
        idx_duplicate = df_clean.loc[code_match & contract_invalid].index.values
        df_clean = df_clean.drop(idx_duplicate, axis="index")
    

# test
tests.test_all_memberships_are_filled(df_clean, "student_membership")
tests.test_all_centers_are_filled(df_clean, "student_center")
tests.test_all_areas_are_filled(df_clean, "student_area")
tests.test_cpt_members_in_cpt_area(df_clean, "is_cpt", "student_center", "student_area")
tests.test_noncpt_members_in_noncpt_area(df_clean, "is_cpt")
tests.test_one_code_is_one_name(df_clean, "student_code", "student_name")


# save df
filename = ("coco member.xlsx").replace(" ", "_")
output_path = Path("output", folder_path.stem)

if not os.path.exists(full_filepath := output_path / filename):
    try:
        os.mkdir(output_path)
    except FileExistsError:
        pass
    df_clean.to_excel(full_filepath, engine="xlsxwriter", index=False)
    print("File saved.")
else:
    print("File already exist.")