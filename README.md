# nazk_parser

Парсер декларацій з сайту НАЗК

Як користуватись?

1. Скачати портативний Python 2.7 звідси -
2. Розпакувати архів, покласти папку Python27 в папку з файлами з цього репозиторію
3. Відредагувати файл declaration_ids.txt і помістити туди потрібні id декларацій (по одній на рядок, у кінці файлу має бути 1 пустий рядок)
4. Запустити файл get_declarations.bat
5. Зачекати закриття командого рядка
6. З'явиться CSV файл з кодуванням UTF-8, який можна імпортувати в Excel через Data - From Text

Пояснення полів:

0. Модифікатори /no_info, /until_2014, /in_2014, /in_2015, /all - немає інформації про дату набуття, до 2014 року, в 2014-му році, в 2015-му році, загалом
1. land, houses, appartments, other_land - площа земельних ділянок, будинків, квартир, іншої нерухомості (в т.ч. паркомісць і дач)
2. personalty - приблизна вартість рухомості (якщо не вказана вартість, то 120 000 грн за один рядок в декларації без залежності від кількості одиниць)
3. transport - приблизна вартість транспорту (якщо не вказана вартість, то 120 000 грн за один рядок в декларації без залежності від кількості одиниць)
4. transport_amount_cars - кількість легкових автомобілів
5. securities - вартість цінних паперів
6. corporate - вартість корпоративних прав
7. corporate_amount - кількість компаній, кінцевим бенефіціаром яких є декларант
8. income - доходи
9. Модифікатори /salary, /presents, /other - зарплатня, подарунки, інше, загалом
10. money - грошові активи
11. Модифікатори /bank, /cash, /other, /all - у банку, готівка, інше, загалом
