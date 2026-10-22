from datetime import date, timedelta

# テスト対象の関数
def search_for_employees_with_specified_birthday(birthday:date, employees:list[tuple[str, date]]):
    found_employees: list[tuple[str, date]] = [
        employee for employee in employees if employee[1] == birthday
    ]

    return found_employees

def generate_all_days_in_year(year:int) -> list[date]:
    start = date(year, 1, 1)
    end = date(year+1, 1, 1)
    return [start + timedelta(i) for i in range((end - start).days)]
    

def test_search_for_employees_with_specified_birthday():
    # 入力をgenerator無しの全網羅で作る
    dates = generate_all_days_in_year(2026)
    employees_with_birthday:list[tuple[str, date]] = [
        ('employees' + str(i), dates[i]) for i in range(len(dates))
    ]

    # 処理を行う
    found = []
    for trg_date in dates:
        found += search_for_employees_with_specified_birthday(trg_date, employees_with_birthday)
    
    # propertyをassertする
    assert len(employees_with_birthday) == len(found)

if __name__ == "__main__":
    print(generate_all_days_in_year(2026), len(generate_all_days_in_year(2026)))