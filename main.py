import matplotlib as mpl
import matplotlib.pyplot as plt
from math import cos, tan, asin, sin, sqrt, radians, pi

mpl.use('TkAgg')


class Raio:
    def __init__(self, angulo, x, y):
        self.angulo = angulo
        self.x = x
        self.y = y

    def limitar(self, esquerda, direita, superior, inferior):
        self.esquerda = esquerda
        self.direita = direita
        self.superior = superior
        self.inferior = inferior

    def _equacao_reta(self, x):
        ponto_y =  tan(self.angulo) * (x - self.x) + self.y

        if (ponto_y >= self.inferior) and (ponto_y <= self.superior):
            return ponto_y
    
    @property
    def valores_x(self):
        return [valor_xy[0] for valor_xy in self.valores_xy]

    @property    
    def valores_y(self):
        return [valor_xy[1] for valor_xy in self.valores_xy]

    @property
    def valores_xy(self):
        resolucao = 100
        valores_x = [x/resolucao for x in range(int(self.esquerda*resolucao), int(self.direita*resolucao + 1))]
        valores_y = [self._equacao_reta(x) for x in valores_x]
        valores = []

        for x, y in zip(valores_x, valores_y):
            if y != None:
                valores.append((x, y))
        
        return valores
        
    @property
    def final_x(self):
        return self.valores_x[-1]

    @property
    def final_y(self):
        return self.valores_y[-1]
        
    
# Coeficientes para simulacao
n1 = 1
n2 = 1.48
n3 = 1.465

# Dados plot
inicio_plot = -2

# Dados da Fibra otica
inicio_fibra = 0
final_fibra = 90
casca_superior = 4
casca_inferior = -4

# Definir angulo de incidencia inicial - orientando corretamente
#angulo_inicial = (sqrt(n2**2 - n3**2) / n1)
angulo_inicial = radians(40)

# Calcular primeiro raio incidente
raio_incidente_ar = Raio(angulo_inicial, 0, 0)
raio_incidente_ar.limitar(inicio_plot, inicio_fibra, casca_superior, casca_inferior)
plt.plot(raio_incidente_ar.valores_x, raio_incidente_ar.valores_y, color='red')

# Calcular raio refratado na fibra de vidro
angulo_refracao_fibra = asin((n1/n2) * sin(angulo_inicial))
raio_refratado_fibra = Raio(angulo_refracao_fibra, raio_incidente_ar.final_x, raio_incidente_ar.final_y)
raio_refratado_fibra.limitar(inicio_fibra, final_fibra, casca_superior, casca_inferior)

plt.plot(raio_refratado_fibra.valores_x, raio_refratado_fibra.valores_y, color='red')
print(raio_incidente_ar.final_x, raio_incidente_ar.final_y)

# Calcular raio refratado para a casca
try:
    angulo_refracao_casca = asin((n2/n3) * sin(pi/2 - angulo_refracao_fibra))
    print(angulo_refracao_casca)
    raio_refratado_casca = Raio(angulo_refracao_casca, raio_refratado_fibra.final_x, raio_refratado_fibra.final_y)
    raio_refratado_casca.limitar(raio_refratado_fibra.final_x, final_fibra, casca_superior + 2, casca_inferior - 2)
    plt.plot(raio_refratado_casca.valores_x, raio_refratado_casca.valores_y, color='red')

    final_fibra = raio_refratado_casca.final_x
except:
    # Calcular raio refletido na fibra de vidro
    angulo_reflexao_fibra = -(angulo_refracao_fibra)  
    raio_refletido_fibra = Raio(angulo_reflexao_fibra, raio_refratado_fibra.final_x, raio_refratado_fibra.final_y)
    raio_refletido_fibra.limitar(raio_refratado_fibra.final_x, final_fibra, casca_superior, casca_inferior)
    plt.plot(raio_refletido_fibra.valores_x, raio_refletido_fibra.valores_y, color='blue')


# Delimitar fibra
plt.plot([inicio_fibra, inicio_fibra], [casca_inferior - 2, casca_superior + 2], color='black')

# Casca fibra
plt.plot([inicio_fibra, final_fibra], [casca_superior, casca_superior], color='black')
plt.plot([inicio_fibra, final_fibra], [casca_inferior, casca_inferior], color='black')

# linha orientacao
plt.plot([inicio_plot, final_fibra], [0, 0], color='black', linestyle='dashed')

plt.show()