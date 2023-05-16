import subprocess
import requests


def check_website(url):
    try:
        # Ejecutar el comando ping
        process = subprocess.Popen(["ping", "-c", "1", url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Esperar hasta que el proceso se complete
        process.wait()
        # Leer la salida del comando
       
        output, error = process.communicate()
        # Comprobar si el comando se ejecutó correctamente
        if process.returncode == 0:
            print(f"{url} responde a ping.")
            url2 = "https://" + url;
            response = requests.get(url2)
            if response.status_code == 200:
                print(f"{url} está activo.")
            else:
                print(f"{url} está caído con un código de estado {response.status_code}.")
        else:
            print(f"{url} está caído o puede tener deshabilitado el ping")
            url2 = "https://" + url;
            try:
                response = requests.get(url2)
                if response.status_code == 200:
                    print(f"{url} está activo.")
                else:
                    print(f"{url} está caído con un código de estado {response.status_code}.")
            except requests.exceptions.RequestException as e:
                print("Error de conexion con request")
    
    except subprocess.CalledProcessError as e:
        print(f"No se pudo ejecutar el comando ping para {url}. Error: {e}")




# Ejemplo de uso:
print("REPORTE CONECTIVIDAD\n\n")
check_website("moodlesedesur.unsa.edu.ar")
print("---------------------------\n\n")
check_website("obras.unsa.edu.ar")
print("---------------------------\n\n")
check_website("sedesur.unsa.edu.ar")
print("---------------------------\n\n")
check_website("cooperacion.unsa.edu.ar")
print("---------------------------\n\n")
check_website("www.unsa.edu.ar")
print("---------------------------\n\n")
check_website("revistas.natura.unsa.edu.ar")
print("---------------------------\n\n")
check_website("iemtar.unsa.edu.ar")
print("---------------------------\n\n")
check_website("moodlerec.unsa.edu.ar")
print("---------------------------\n\n")
check_website("ticservicios.unsa.edu.ar")
