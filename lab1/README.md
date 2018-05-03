# LAB1

## Варіант 3

ПЗ для пошуку e-mail. Реалізувати проходження по сторінкам з набору url, які
задані у вхідному xml-файлі, а також по сторінкам, на які є посилання з цих
сторінок з заданою глибиною вкладеності. На всіх цих сторінках знайти всі
e-mail-адреси та зберігти їх у файл в форматі xml. Урахувати те, що
e-mail-адреси можуть бути записані у прихованому форматі, наприклад
name(at)example.org.

## Приклад вхідних даних

    <data>
	   <url>https://some.ua/url/</url>
	   <url>https://onemoreurl.com/</url>
    </data>

## Приклад вихідних даних

    <?xml version="1.0" encoding="utf-8"?>
    <data>
        <email>
            email1@gmail.org
        </email>
        <email>
            email2@github.com
        </email>
        <email>
            octocat@nowhere.com
        </email>
    </data>


## coverage тести

	Name             Stmts   Miss  Cover   Missing
	----------------------------------------------	
	find_emails.py      36      0   100%
