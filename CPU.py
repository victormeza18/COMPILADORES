# CODIGO
class Instruction:
    def __init__(self, name="", code=0, length=0):
        self.name = name
        self.code = code
        self.length = length

    def display(self):
        print(f"{self.name}, {self.code}, {self.length}")

    def get_code(self):
        return self.code

    def get_name(self):
        return self.name

# Clase ADD que hereda de Instruction
class ADD(Instruction):
    def __init__(self, name="", code=0, length=0, operand1=0, operand2=0):
        super().__init__(name, code, length)
        self.operand1 = operand1
        self.operand2 = operand2

    def get_operand1(self):
        return self.operand1

    def get_operand2(self):
        return self.operand2

# Clase MOV que hereda de Instruction
class MOV(Instruction):
    def __init__(self, name="", code=0, length=0, value=0, regist="", address=""):
        super().__init__(name, code, length)
        self.value = value
        self.regist = regist
        self.address = address

    def get_value(self):
        return self.value

    def display(self):
        if self.regist and self.address:
            print(f"{self.regist}, {self.address}")
        else:
            print(f"{self.name}, {self.value}, {self.regist}")

# Clase ALU (Unidad Aritmético Lógica)
class ALU:
    def __init__(self, operand1=0, operand2=0):
        self.operand1 = operand1
        self.operand2 = operand2

    def add(self, op1, op2):
        # Simula la suma física que en C++ se hacía con ensamblador
        return op1 + op2

# Clase Program que almacena la secuencia de instrucciones
class Program:
    def __init__(self):
        self.instructions = [None] * 10 # Arreglo fijo de 10 instrucciones

    def add_instruction(self, instruction, position):
        if 0 <= position < len(self.instructions):
            self.instructions[position] = instruction

    def get_instruction(self, position):
        return self.instructions[position]

# Clase CU (Unidad de Control) - Máquina de estados (Autómata)
class CU:
    def __init__(self, status="idle"):
        self.status = status # Estados: idle, fetch, decode, execute

    def fetch(self, program, position):
        self.status = "fetch"
        return program.get_instruction(position)

    def decode(self, instruction):
        self.status = "decode"
        if instruction is not None:
            return instruction.get_code()
        return -1

    def execute(self, code, instruction=None, alu=None):
        self.status = "execute"
        if code == 50:
            if instruction and instruction.get_name() == "MOV":
                print(f"Ejecutando MOV: Moviendo valor {instruction.get_value()} al registro {instruction.regist}")
            else:
                print("Inicio del programa")
        elif code == 51:
            print("Fin de ejecución del programa")
        elif code == 80:
            print("Ejecutando ADD...")
            if isinstance(instruction, ADD) and alu:
                # Utilizamos la ALU para realizar la suma real
                resultado = alu.add(instruction.get_operand1(), instruction.get_operand2())
                print(f"Suma realizada por la ALU: {resultado}")
        else:
            print(f"Código de instrucción {code} no reconocido.")

# Clase InstructionSet (Conjunto de instrucciones disponibles)
class InstructionSet:
    def __init__(self):
        self.set = [None] * 10
        self.index = 0

    def add_instruction(self, instruction):
        if self.index < len(self.set):
            self.set[self.index] = instruction
            self.index += 1

    def get_instruction(self, pos):
        return self.set[pos]

# Ejecución principal (Equivalente al Main.cpp)
if __name__ == "__main__":
    # 1. Creación de instrucciones básicas
    i1 = Instruction()
    i2 = Instruction("MOV", 50, 3)
    
    i1.display()
    i2.display()

    # 2. Uso del InstructionSet
    instruction_set = InstructionSet()
    instruction_set.add_instruction(i2)
    i1 = instruction_set.get_instruction(0)
    i1.display()

    # 3. Creación de instrucciones específicas
    start = Instruction("START", 50, 1)
    stop = Instruction("STOP", 51, 1)
    add = ADD("ADD", 80, 3, 60, 12) # Sumará 60 + 12
    
    # 4. Carga de instrucciones en el Programa
    program = Program()
    program.add_instruction(start, 0)
    program.add_instruction(add, 1)
    program.add_instruction(stop, 2)

    print(program.get_instruction(0).get_name())
    print(program.get_instruction(1).get_name())
    print(program.get_instruction(2).get_name())

    # 5. Inicialización de la Unidad de Control (CU) y ALU
    cu = CU()
    alu = ALU()

    print("\n--- INICIANDO CICLO DE RELOJ (AUTÓMATA) ---")
    pc = 0 # Program Counter
    while True:
        # Estado FETCH (Búsqueda)
        current_instruction = cu.fetch(program, pc)
        
        if current_instruction is None:
            break # Evita errores si la memoria está vacía

        # Estado DECODE (Decodificación)
        opcode = cu.decode(current_instruction)

        # Estado EXECUTE (Ejecución)
        cu.execute(opcode, current_instruction, alu)

        if opcode == 51: # Código de STOP
            break
            
        pc += 1 # Incrementar Program Counter

    print("\n--- PRUEBA DE MOVIMIENTO A REGISTROS ---")
    # En Python no usamos el ensamblador __asm__, simulamos el movimiento a registros
    mov1 = MOV("MOV", 17, 3, value=10, regist="eax")
    mov2 = MOV("MOV", 21, 3, value=20, regist="ebx")
    
    print(f"Valor a mover 1: {mov1.get_value()}")
    print(f"Valor a mover 2: {mov2.get_value()}")
    
    # Simulación de la suma de registros (eax + ebx) con la ALU
    total = alu.add(mov1.get_value(), mov2.get_value())
    print(f"Suma de registros simulados = {total}")
