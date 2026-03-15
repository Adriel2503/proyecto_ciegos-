import random
import time

def sortear_libro():
    """
    Función que genera un número aleatorio del 1 al 30 para el sorteo de un libro
    """
    print("🎲 ¡SORTEO DE LIBRO! 🎲")
    print("=" * 30)
    print("Generando número aleatorio del 1 al 30...")
    
    # Pequeña pausa para crear suspense
    time.sleep(1)
    print(".")
    time.sleep(0.5)
    print("..")
    time.sleep(0.5)
    print("...")
    time.sleep(0.5)
    
    # Generar número aleatorio del 1 al 30
    numero_ganador = random.randint(1, 30)
    
    print(f"\n🎉 ¡EL NÚMERO GANADOR ES: {numero_ganador}! 🎉")
    print("=" * 30)
    print(f"¡Felicidades al participante número {numero_ganador}!")
    
    return numero_ganador

def main():
    """
    Función principal del programa
    """
    try:
        while True:
            sortear_libro()
            
            print("\n¿Quieres hacer otro sorteo? (s/n): ", end="")
            respuesta = input().lower().strip()
            
            if respuesta in ['n', 'no']:
                print("\n¡Gracias por usar el sorteo de libros! 📚")
                break
            elif respuesta in ['s', 'si', 'sí', 'yes', '']:
                print("\n" + "="*50 + "\n")
                continue
            else:
                print("Por favor responde 's' para sí o 'n' para no.")
                continue
                
    except KeyboardInterrupt:
        print("\n\n¡Sorteo cancelado! ¡Hasta luego! 👋")
    except Exception as e:
        print(f"\nError inesperado: {e}")

if __name__ == "__main__":
    main()
