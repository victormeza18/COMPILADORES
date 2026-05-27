#include <iostream>
#include <string>
#include <cctype>

using namespace std;

// Clase que implementa el Autómata Finito (FSA) para validar números
class NumberValidatorFSA {
private:
    int currentState;

    // Función auxiliar para verificar si un carácter es un dígito
    bool isDigit(char c) {
        return isdigit(c);
    }

public:
    NumberValidatorFSA() {
        currentState = 12; // Estado inicial según el diagrama
    }

    void reset() {
        currentState = 12;
    }

    // Método que procesa la cadena de texto carácter por carácter
    bool validate(const string& input) {
        reset();
        
        for (int i = 0; i < input.length(); i++) {
            char c = input[i];

            switch (currentState) {
                case 12:
                    if (isDigit(c)) currentState = 13;
                    else return false;
                    break;
                case 13:
                    if (isDigit(c)) currentState = 13;
                    else if (c == '.') currentState = 14;
                    else if (c == 'E') currentState = 16;
                    else return false; 
                    break;
                case 14:
                    if (isDigit(c)) currentState = 15;
                    else return false;
                    break;
                case 15:
                    if (isDigit(c)) currentState = 15;
                    else if (c == 'E') currentState = 16;
                    else return false;
                    break;
                case 16:
                    if (c == '+' || c == '-') currentState = 17;
                    else if (isDigit(c)) currentState = 18;
                    else return false;
                    break;
                case 17:
                    if (isDigit(c)) currentState = 18;
                    else return false;
                    break;
                case 18:
                    if (isDigit(c)) currentState = 18;
                    else return false;
                    break;
                default:
                    return false;
            }
        }
        
        // Los estados 13, 15 y 18 son los que en el diagrama llevan a un estado de aceptación 
        // (20, 21 y 19 respectivamente) cuando se recibe un carácter "other" (fin de palabra).
        return (currentState == 13 || currentState == 15 || currentState == 18);
    }
};

int main() {
    NumberValidatorFSA fsa;
    
    // Casos de prueba
    string testCases[] = {
        "123",        // Válido (entero)
        "3.14159",    // Válido (decimal)
        "6.02E23",    // Válido (exponencial)
        "6.02E+23",   // Válido (exponencial con signo)
        "12.",        // Inválido (requiere dígito después del punto)
        "E23",        // Inválido (debe iniciar con dígito)
        "12.3E-",     // Inválido (requiere dígito después del signo en exponencial)
        "abc"         // Inválido (letras)
    };

    cout << "--- PRUEBA DEL AUTÓMATA (NUMBERS FSA) ---" << endl;
    for (const string& test : testCases) {
        if (fsa.validate(test)) {
            cout << "La cifra '" << test << "' es VALIDA." << endl;
        } else {
            cout << "La cifra '" << test << "' es INVALIDA." << endl;
        }
    }

    return 0;
}
