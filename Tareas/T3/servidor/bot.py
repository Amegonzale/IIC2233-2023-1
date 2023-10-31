import random
import metodos_auxiliares as m


class Bot():
    def __init__(self, prob_dudar, prob_anunciar):
        super().__init__()
        self.prob_dudar = prob_dudar
        self.prob_anunciar = prob_anunciar

    def play(self, valor_anunciado, parte, player, players_info, valor_paso, maximo_anunciado):
        # Editar las cosas aca funciona pq los diccionarios del sv se editan si los modifico aca
        # Primero intenta dudar
        if random.random() <= self.prob_dudar and not parte:
            return self.dudar(player, valor_anunciado, players_info)
        else:
            # Si no funciona primero cambia sus dados
            self.cambiar_dados(player)
            accion = ''
            # Esto lo hago pq cuando es el primer turno de la ronda el max parte en cero
            # pero los numeros validos de suma van del 2 al 12
            if maximo_anunciado == 0:
                maximo_anunciado = 1

            # Luego trata de anunciar
            if random.random() <= self.prob_anunciar:
                # no puede anunciar nada sobre 12 si es el max anunciado
                if maximo_anunciado != 12:
                    valor = random.randint(maximo_anunciado + 1, 12)
                    # anuncia solo si es distinto de 12
                    if valor != 12:
                        accion = 'anunciar'
            # anuncia
            if accion == 'anunciar':
                return self.anunciar_valor(player, valor_anunciado, valor, players_info)
            # si no anuncia pasa
            else:
                return self.pasar_turno(valor_anunciado, valor_paso, player, players_info)

    def dudar(self, player, valor_anunciado, players_info):
        m.log_dudar('', '', '', player=player)
        if valor_anunciado['mintiendo']:
            mentiroso = m.get_player_info(valor_anunciado['id'], players_info)
            return ['dudar', [mentiroso, 'mintiendo']]
        else:
            return ['dudar', [player, '']]

    def cambiar_dados(self, player):
        m.log_cambiar_dados(player)
        dado1, dado2 = m.random_dados()
        player['dado1'] = dado1
        player['dado2'] = dado2

    def anunciar_valor(self, player, valor_anunciado, valor, players_info):
        m.log_anunciar_valor('', '', '', valor, player=player)
        valor_anunciado['valor'] = valor
        valor_anunciado['id'] = player['id']
        valor_anunciado['mintiendo'] = m.miente(valor, player['id'], players_info)
        return ['anunciar valor', [valor]]

    def pasar_turno(self, valor_anunciado, valor_paso, player, players_info):
        m.log_pasar_turno('', '', '', player=player)
        valor_anunciado['valor'] = valor_paso
        valor_anunciado['id'] = player['id']
        valor_anunciado['mintiendo'] = m.miente(valor_paso, player['id'], players_info)
        return ['pasar', []]
