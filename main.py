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
        student_code=lambda df_: module.create_student_code(df_),
        student_membership=lambda df_: module.create_student_membership(df_),
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
    # ! drop duplicated member based on student code and end date
    # somehow there is a student with different start date but same end date
    .drop_duplicates(subset=["student_code", "end_date"], keep="first")
    # ! drop unnecessary cols
    .drop(
        columns=[
            "gender", "home", "work", "end_level", "on_track", "course_status", 
            "personal_tutor", "first_name", "last_name", "center_name",
        ]
    )
)

# test
tests.test_all_memberships_are_filled(df_clean, "student_membership")
tests.test_all_centers_are_filled(df_clean, "student_center")
tests.test_all_areas_are_filled(df_clean, "student_area")
tests.test_cpt_members_in_cpt_area(df_clean, "is_cpt", "student_center", "student_area")
tests.test_noncpt_members_in_noncpt_area(df_clean, "is_cpt")


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