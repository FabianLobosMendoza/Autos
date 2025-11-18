#include <stdio.h>
#include <ctype.h>

int main() {
    char letra;

    // Solicitar al usuario que ingrese una letra
    printf("Ingrese una letra: ");
    scanf(" %c", &letra);
    
    //verificar que no sea un signo
    if (ispunct(letra)){
        printf(" no puto! ");
    }

    // Convertir la letra a minúscula para simplificar la comparación
    letra = tolower(letra);

    // Verificar si es una letra del alfabeto
    if ((letra >= 'a' && letra <= 'z')) {
        // Comprobar si es una vocal
        if (letra == 'a' || letra == 'e' || letra == 'i' || letra == 'o' || letra == 'u') {
            printf("La letra '%c' es una vocal.\n", letra);
            printf("test1");
        } else {
            printf("La letra '%c' es una consonante.\n", letra);
        }
    } else {
        printf("El caracter ingresado no es una letra.\n");
    }

    return 0;
}