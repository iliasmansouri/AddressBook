import streamlit as st
from core.data_handler import AddressBook
from core.browser import Browser
from core.viz_utils import draw_pie


def add_record():
    with st.form("add_record_form"):
        name = st.text_input("Name")
        gender = st.selectbox(
            "Select gender",
            ("Male", "Female"),
        )
        date = st.date_input("Date", format="YYYY/MM/DD")
        submitted = st.form_submit_button("Submit")
        if submitted and name and gender and date:
            return (name, gender, date)
        else:
            st.write("Fill in all 3 fields")
            return False


def delete_record():
    with st.sidebar.form("delete_record_form"):
        name = st.selectbox(
            "Which name do you want to delete?",
            st.session_state.address_book.get_names(),
        )
        deleted = st.form_submit_button("Delete")
        if deleted and name:
            return name
        else:
            return False


def draw_stats():
    male_count = st.session_state["browser"].count_records("male")
    female_count = st.session_state["browser"].count_records("female")

    draw_pie(male_count, female_count)


def calculate_age_for_2_names():
    left_column, right_column = st.columns(2)

    with left_column:
        name_1 = st.selectbox(
            "Select first name:",
            st.session_state.address_book.get_names(),
        )
    with right_column:
        name_2 = st.selectbox(
            "Select second name:",
            st.session_state.address_book.get_names(),
        )

    return st.session_state.browser.get_age_difference(name_1, name_2)


if __name__ == "__main__":
    address_book = AddressBook("./assets/data.txt")

    if "address_book" not in st.session_state:
        st.session_state["address_book"] = address_book

    if "browser" not in st.session_state:
        st.session_state["browser"] = Browser(address_book)

    record_to_add = add_record()
    record_to_delete = delete_record()

    if record_to_add:
        name = record_to_add[0]
        gender = record_to_add[1]
        date = record_to_add[2].strftime("%d/%m/%y")
        try:
            st.session_state.address_book.add_record(name, gender, date)
            # force the code inside form_fn to rerun
            st.rerun()
        except Exception as e:
            st.error(str(e))

    if record_to_delete:
        name = record_to_delete
        try:
            st.session_state.address_book.delete_record(name)
            # force the code inside form_fn to rerun
            st.rerun()
        except Exception as e:
            st.error(str(e))

    st.write(st.session_state.address_book.get_df())

    if st.button("Save addressbook"):
        st.session_state.address_book.save_records("./assets/records.txt")

    draw_stats()

    st.write(f"Most recent record is: {st.session_state.browser.get_youngest_record()}")
    st.write(f"Most oldest record is: {st.session_state.browser.get_oldest_record()}")

    st.write(calculate_age_for_2_names())
