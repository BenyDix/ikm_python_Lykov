"""
Программа для построения цепочки из костей домино.
Использует двухсвязный список для хранения последовательности.
"""


class DominoNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def append(self, node):
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
        self.size += 1
    
    def remove_last(self):
        if self.tail is None:
            return
        
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        self.size -= 1
    
    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(f"{current.left}{current.right}")
            current = current.next
        return result


def parse_dominoes(input_string):
    if not input_string or not input_string.strip():
        return None, "строка не может быть пустой"
    
    input_string = input_string.replace(',', ' ')
    parts = input_string.split()
    
    if not parts:
        return None, "не найдено ни одной кости домино"
    
    dominoes = []
    seen = set()
    
    for i, part in enumerate(parts):
        if len(part) != 2:
            return None, f"кость '{part}' должна состоять из ровно 2 цифр"
        
        if not (part[0].isdigit() and part[1].isdigit()):
            return None, f"кость '{part}' содержит нецифровые символы"
        
        left = int(part[0])
        right = int(part[1])
        
        if left < 0 or left > 6 or right < 0 or right > 6:
            return None, f"кость '{part}' содержит цифры вне диапазона 0-6"
        
        normalized = tuple(sorted((left, right)))
        if normalized in seen:
            return None, f"кость '{part}' повторяется"
        seen.add(normalized)
        
        dominoes.append((left, right))
    
    return dominoes, None


def find_chain(dominoes):
    if not dominoes:
        return False, None
    
    n = len(dominoes)
    used = [False] * n
    chain = DoublyLinkedList()
    
    # Поиск с возвратом: перебираем все варианты размещения костей,
    # пробуя как прямое, так и перевернутое положение каждой кости
    def backtrack(last_value, used_count):
        if used_count == n:
            return True
        
        for i in range(n):
            if used[i]:
                continue
            
            left, right = dominoes[i]
            
            if last_value is None or left == last_value:
                chain.append(DominoNode(left, right))
                used[i] = True
                if backtrack(right, used_count + 1):
                    return True
                chain.remove_last()
                used[i] = False
            
            if last_value is None or right == last_value:
                chain.append(DominoNode(right, left))
                used[i] = True
                if backtrack(left, used_count + 1):
                    return True
                chain.remove_last()
                used[i] = False
        
        return False
    
    if backtrack(None, 0):
        return True, chain
    return False, None


def show_menu():
    print("\n" + "="*50)
    print("ПРОГРАММА ДЛЯ РАБОТЫ С ДОМИНО")
    print("="*50)
    print("1. Ввести кости домино и проверить возможность построения цепочки")
    print("2. Выйти из программы")
    print("-"*50)


def get_user_input():
    print("\nВведите кости домино в формате: 02 04 42")
    print("(каждая кость - две цифры от 0 до 6, разделители - пробелы или запятые)")
    print("Примеры: 31 00 13  или  02,04,42")
    
    user_input = input("> ").strip()
    return user_input if user_input else None


def process_dominoes(input_string):
    dominoes, error_message = parse_dominoes(input_string)
    
    if dominoes is None:
        print(f"Ошибка: {error_message}")
        return False
    
    print(f"\nВведены кости: {', '.join(f'{l}{r}' for l, r in dominoes)}")
    print(f"Количество костей: {len(dominoes)}")
    
    success, chain = find_chain(dominoes)
    
    if not success:
        print("\nРезультат: НЕЛЬЗЯ построить цепочку из данных костей")
        return True
    
    chain_list = chain.to_list()
    print(f"\nРезультат: можно, {', '.join(chain_list)}")
    return True


def main():
    while True:
        show_menu()
        choice = input("Выберите пункт меню (1-2): ").strip()
        
        if choice == "1":
            input_data = get_user_input()
            if input_data is not None:
                process_dominoes(input_data)
            else:
                print("Ошибка: ввод не может быть пустым!")

            input("\nНажмите Enter для продолжения...")
            
        elif choice == "2":
            print("\nДо свидания!")
            break
            
        else:
            print("\nОшибка: неверный выбор! Пожалуйста, выберите 1 или 2.")
            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()