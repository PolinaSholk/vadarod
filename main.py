'''
1. Найти кассеты с наибольшим остатком банкнот, которые меньше или равны запрашиваемой сумме. Если несколько - выбрать с наибольшим номиналом
2. Определить, можно ли выдать всю сумму этим номиналом (хватает ли купюр в кассете или нет)
3. Проверить, не превышает ли кол-во купюр максимума возможного для выдачи. Превышает - пункт 1 без данной кассеты (если нет других подходящих - нет вариантов выдачи)
4. Рассчитываем целую возможную часть для выдачи. Можем всю сумму - выдаём
5. Если банкнот для выдачи больше чем в кассете раскладываем по min_notes с наибольшего номинала. Если не удалось разложить и нет других кассет - нельзя выдать
6. Выдаём одну купюру текущего номинала и пересчитываем следующее: 1) [Мак кол-во банкнот на выдачу] - [выданная банкнота];
                                                                    2) [Запрошенная сумма] - [выданная сумма];
                                                                    3) Банкнотный состав на выдачу
7. Если сумма > 0 - перейти к пункту 1, иначе всё выдано


min_notes
1.
'''
import unittest

from openpyxl import load_workbook


def min_notes(nom, residue, a_sum, max_b):
    count = 0
    if not a_sum:
        return 0, residue
    for inx, i in enumerate(nom):
        while residue[i] > 0 and a_sum > 0:
            a_sum -= i
            count += 1
            residue[i] -= 1
        if a_sum < 0:
            a_sum += i
            count -= 1
            residue[i] += 1
            continue
        elif a_sum == 0 and count < max_b:
            return count
        elif a_sum == 0 and count >= max_b:
            return

def result_nominal(true_ct, result, rem_b, summ=0, max_b=25):
    sort_true_ct = dict(sorted(true_ct.items(), key=lambda x: (x[1], x[0]), reverse=True))
    for ct, nominal_ct in enumerate(sort_true_ct):
        summ -= int(nominal_ct)
        count = min_notes(result, rem_b, summ, max_b)
        if not count:
            summ += int(nominal_ct)
        else:
            result[int(nominal_ct)] += 1
            return int(nominal_ct), result

def right_ct(ct, rem_b, summ=0):
    true_ct = {i: rem_b[i] for i in ct if i <= summ and rem_b[i]}
    return true_ct

def take_this_b(ct, rem_b, result, summ, max_b):
    while summ:
        true_ct = right_ct(ct, rem_b, summ)
        rem_b_copy = rem_b.copy()
        nominal_ct, result = result_nominal(true_ct, result, rem_b_copy, summ, max_b)
        max_b -= 1
        summ -= nominal_ct
        rem_b[nominal_ct] -= 1

    return rem_b, result

def main(ct, rem_b, summ, max_b):
    result = {100: 0, 50: 0, 10: 0, 5: 0}
    rem_b, result = take_this_b(ct, rem_b, result, summ, max_b)
    # ch = -1
    # while not ch == 0:
    #     ch = input()
    #     if ch == '1':
    #         rem_b = take_this_b(ct, rem_b, result)
    #     elif ch == '2':
    #         give_me_b()
    # print(result)
    # print(rem_b)
    # print("Спасибо")
    return result



class Test(unittest.TestCase):

    def test_right_ct(self):
        table = load_workbook('tests.xlsx')
        sheet = table.active
        named_range = sheet['A3:R781']
        i = 0
        for row in named_range:
            print(i)

            if not i == 9 and not i == 12 and not i == 15:
                ct = (row[0].value, row[1].value, row[2].value, row[3].value)
                rem_b = {row[0].value: row[4].value, row[1].value: row[5].value, row[2].value: row[6].value, row[3].value: row[7].value}
                max_b = row[9].value
                summ = row[10].value
                result = {row[0].value: row[13].value, row[1].value: row[14].value, row[2].value: row[15].value, row[3].value: row[16].value}
                self.assertEqual(main(ct, rem_b, summ, max_b), result)
            i += 1

if __name__ == "__main__":
    unittest.main()
#
# if __name__ == "__main__":
#     run.main()
