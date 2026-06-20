"""
Программа для определения минимальной взятки для получения лицензии.
"""


class Official:
    def __init__(self, id, bribe):
        self.id = id
        self.bribe = bribe
        self.children = []


def parse_input(input_string):
    lines = input_string.strip().split('\n')
    if not lines or not lines[0].strip():
        return None, "пустой ввод"
    
    try:
        n = int(lines[0].strip())
        if n <= 0:
            return None, "количество чиновников должно быть положительным"
    except ValueError:
        return None, "некорректное количество чиновников"
    
    if len(lines) < n + 1:
        return None, f"недостаточно данных: ожидается {n} строк с взятками"
    
    officials = {}
    
    for i in range(1, n + 1):
        parts = lines[i].strip().split()
        if len(parts) != 2:
            return None, f"строка {i}: ожидается 2 числа (id и взятка)"
        
        try:
            id = int(parts[0])
            bribe = int(parts[1])
            if bribe < 0:
                return None, f"взятка не может быть отрицательной"
            officials[id] = Official(id, bribe)
        except ValueError:
            return None, f"строка {i}: некорректные числа"
    
    if len(officials) != n:
        return None, "обнаружены дублирующиеся id чиновников"
    
    return officials, None


def parse_relations(input_string, officials):
    if not input_string or not input_string.strip():
        return None, "не указаны отношения подчинения"
    
    parts = input_string.strip().split()
    
    if len(parts) % 2 != 0:
        return None, "каждая пара должна содержать начальника и подчиненного"
    
    edges = []
    has_parent = set()
    parent_count = {}
    
    for i in range(0, len(parts), 2):
        try:
            boss_id = int(parts[i])
            sub_id = int(parts[i + 1])
            
            if boss_id not in officials:
                return None, f"чиновник с id {boss_id} не найден"
            if sub_id not in officials:
                return None, f"чиновник с id {sub_id} не найден"
            
            edges.append((boss_id, sub_id))
            has_parent.add(sub_id)
            
            parent_count[sub_id] = parent_count.get(sub_id, 0) + 1
            if parent_count[sub_id] > 1:
                return None, f"чиновник {sub_id} имеет более одного начальника"
            
        except ValueError:
            return None, "некорректные id в отношениях"
    
    graph = {id: [] for id in officials}
    for boss_id, sub_id in edges:
        graph[boss_id].append(sub_id)
    
    visited = set()
    recursion_stack = set()
    
    def has_cycle(node_id):
        if node_id in recursion_stack:
            return True
        if node_id in visited:
            return False
        
        visited.add(node_id)
        recursion_stack.add(node_id)
        
        for child_id in graph[node_id]:
            if has_cycle(child_id):
                return True
        
        recursion_stack.remove(node_id)
        return False
    
    for node_id in officials:
        if node_id not in visited:
            if has_cycle(node_id):
                return None, "обнаружена циклическая зависимость"
    
    for boss_id, sub_id in edges:
        officials[boss_id].children.append(officials[sub_id])
    
    roots = []
    for id, official in officials.items():
        if id not in has_parent:
            roots.append(official)
    
    if len(roots) == 0:
        return None, "нет главного чиновника"
    
    # Пробуем каждый корень как потенциального главного
    # Выбираем тот, из которого достижимы все чиновники
    valid_root = None
    for root in roots:
        visited = set()
        def dfs(node):
            visited.add(node.id)
            for child in node.children:
                dfs(child)
        dfs(root)
        
        if len(visited) == len(officials):
            valid_root = root
            break
    
    if valid_root is not None:
        return valid_root, None
    
    if len(roots) > 1:
        return None, "не все чиновники достижимы из главного"
    
    return None, "не все чиновники достижимы из главного"


def find_min_bribe_and_path(node):
    if not node.children:
        return node.bribe, [node.id]
    
    best_cost = float('inf')
    best_path = None
    
    for child in node.children:
        child_cost, child_path = find_min_bribe_and_path(child)
        total_cost = child_cost + node.bribe
        
        if total_cost < best_cost:
            best_cost = total_cost
            best_path = child_path + [node.id]
    
    return best_cost, best_path


def format_path(path):
    if not path:
        return ""
    
    result = []
    for i, id in enumerate(path):
        if i == len(path) - 1:
            result.append(f"{id} (главный)")
        else:
            result.append(str(id))
    return " → ".join(result)


def show_menu():
    print("\n" + "="*50)
    print("ПРОГРАММА ДЛЯ ПОЛУЧЕНИЯ ЛИЦЕНЗИИ")
    print("="*50)
    print("1. Ввести данные о чиновниках и найти минимальную взятку")
    print("2. Выйти из программы")
    print("-"*50)


def get_tree_data():
    print("\nВведите количество чиновников:")
    try:
        n = int(input("> ").strip())
        if n <= 0:
            print("Ошибка: количество должно быть положительным")
            return None
    except ValueError:
        print("Ошибка: введите целое число")
        return None
    
    print(f"\nВведите данные для {n} чиновников (id и взятка):")
    print("Пример: 1 10")
    lines = [f"{n}"]
    
    for i in range(n):
        line = input(f"Чиновник {i+1}: ").strip()
        if not line:
            print("Ошибка: строка не может быть пустой")
            return None
        lines.append(line)
    
    input_data = '\n'.join(lines)
    officials, error = parse_input(input_data)
    
    if officials is None:
        print(f"Ошибка: {error}")
        return None
    
    print("\nВведите отношения подчинения (начальник подчиненный):")
    print("Пример: 1 2 1 3 2 4")
    relations = input("> ").strip()
    
    root, error = parse_relations(relations, officials)
    if root is None:
        print(f"Ошибка: {error}")
        return None
    
    return root


def process_tree_data(root):
    print(f"\nГлавный чиновник: {root.id}")
    
    cost, path = find_min_bribe_and_path(root)
    
    print(f"\nМинимальная сумма взяток: {cost} у.е.")
    print(f"Порядок получения подписей: {format_path(path)}")


def main():
    while True:
        show_menu()
        choice = input("Выберите пункт меню (1-2): ").strip()
        
        if choice == "1":
            root = get_tree_data()
            if root is not None:
                process_tree_data(root)
            input("\nНажмите Enter для продолжения...")
            
        elif choice == "2":
            print("\nДо свидания!")
            break
            
        else:
            print("\nОшибка: неверный выбор!")
            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()