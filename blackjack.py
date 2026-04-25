# Jogo de blackjack no terminal

import random, time

def baralho() -> dict:
    cartas = {}
    
    naipes = ['♠','♣','♥','♦']
    
    for i in naipes:
        cartas['A' + i] = ''
    
    for i in range(2, 11):
        
        for n in naipes:
            cartas[str(i) + n] = ''
            
    for i in ('J', 'Q', 'K'):
        
        for n in naipes:
            cartas[i + n] = ''
            
    for i in cartas.keys():
        
        if 'A' in i:
            cartas[i] = 1
            
        for n in range(2, 11):
            
            if str(n) in i:
                cartas[i] = n

        if 'J' in i or 'Q' in i or 'K' in i:
            cartas[i] = 10
            
    return cartas

def tirar_carta(cartas: dict) -> tuple:
    
    carta = random.choice(list(cartas.keys()))
    
    valor_carta = cartas[carta]
    
    cartas.pop(carta)
    
    return carta, valor_carta

def mao_jogador(mao: dict, cartas: dict) -> dict:
    
    if len(mao) <= 2:
        for _ in range(2):
            
            carta = tirar_carta(cartas)
            
            mao[carta[0]] = carta[1]
    
    else:
        carta = tirar_carta(cartas)
        
        mao[carta[0]] = carta[1]
        
    return mao
    
def mao_dealer(mao: dict, cartas: dict) -> dict:
    
    carta = tirar_carta(cartas)
    
    mao[carta[0]] = carta[1]
    
    return mao

def mostrar_mao_jogador(mao_jogador: dict) -> int:
    
    time.sleep(0.5)
    
    print('Jogador:', end=' ', flush=True)
    
    soma = 0
    
    As = False
    
    for i in mao_jogador.keys():
        print(i, end=' ', flush=True)
        
        soma += mao_jogador[i]
        
        if 'A' in i:
            As = True
        
        time.sleep(0.5)
        
    if As == True and soma < 11:
        print(f'| {soma}/{soma + 10}')
        
    elif As == True and soma == 11:
        print(f'| {soma + 10}')
        
    else:
        print(f'| {soma}')
        
    return soma
        
def mostrar_mao_dealer(mao_dealer: dict) -> int:
    
    print('\nDealer:', end=' ', flush=True)
    
    soma = 0
    
    As = False
    
    for i in mao_dealer.keys():
        print(i, end=' ', flush=True)
        
        soma += mao_dealer[i]
        
        if 'A' in i:
            As = True
            
        time.sleep(0.5)
        
    if len(mao_dealer) == 1:  
        print('🂠', end=' ', flush=True)
        
    if As == True and soma < 11:
        print(f'| {soma}/{soma + 10}')
        
    elif As == True and soma == 11:
        print(f'| {soma + 10}')
        
    else:
        print(f'| {soma}')
        
    return soma

def acoes(creditos: float, aposta: float, cartas: dict) -> tuple[str, float]:
            
    if creditos >= aposta * 2 and len(cartas) == 2:
        print('\nDouble (d) | Hit (h) | Stand (s)')
        
    else:
        print('\nHit (h) | Stand (s)')
        
    acao = input('\nAção: ').lower()
    
    if acao == 's' or acao == 'h':
        ret = acao
    
    elif creditos >= aposta * 2 and len(cartas) == 2 and acao == 'd':
        ret = acao
        
        aposta *= 2
    
    else: 
        ret = 'e'
        
    return ret, aposta

def blackjack(creditos: float) -> float:
    
    cartas = baralho()
    
    print(f'\nSaldo atual: {creditos}')
    
    if creditos < 5:
        print('\nSaldo insuficiente. Fim de jogo')
        
        return
    
    aposta = float(input('\nAdicione sua aposta: '))
    
    while aposta > creditos or aposta < 5:
        
        if aposta > creditos:
            print(f'\nAposta inválida. A aposta excede o saldo atual ({creditos})')
            
        if aposta < 5:
            print('\nAposta inválida. A aposta deve ser maior que 5 créditos')
            
        aposta = float(input('\nAdicione sua aposta: '))
    
    cartas_jogador = {}        
    cartas_jogador = mao_jogador(cartas_jogador, cartas)
        
    cartas_dealer = {}    
    cartas_dealer = mao_dealer(cartas_dealer, cartas)
    
    mostrar_mao_dealer(cartas_dealer)
    jogador = mostrar_mao_jogador(cartas_jogador)
    
    if jogador == 11 and len(cartas_jogador) == 2 and 1 in cartas_jogador.values():
        
        soma_dealer = sum(cartas_dealer.values())
        
        while soma_dealer < 17:
            nova_carta_dealer = tirar_carta(cartas)
            
            cartas_dealer[nova_carta_dealer[0]] = nova_carta_dealer[1]
            
            soma_dealer += nova_carta_dealer[1]
            
            if 1 in cartas_dealer.values() and soma_dealer <= 11 and soma_dealer + 10 >= 17:
                    As = True
                    
                    break
            
            else:
                As = False
            
        if As == True:
                soma_dealer += 10
                
        if soma_dealer == 21:
            win = None
        
        else:
            creditos += aposta * 1.5
            
            print()
                    
            for i in '✩BLACKJACK✩':
                print(i, end=' ', flush=True)
                
                time.sleep(0.05)
                
            time.sleep(0.4)
            
            print('\n\nPlayer win!')
            
            return creditos
    
    else:
    
        acao = acoes(creditos, aposta, cartas_jogador)
        
        while acao[0] == 'e':
            print('\nAção inválida')
            
            mostrar_mao_dealer(cartas_dealer)
            jogador = mostrar_mao_jogador(cartas_jogador)
            
            acao = acoes(creditos, aposta, cartas_jogador)
            
        aposta = acao[1]
        
        while acao[0] != 's':
            nova_carta_jogador = tirar_carta(cartas)
            
            cartas_jogador[nova_carta_jogador[0]] = nova_carta_jogador[1]
            
            mostrar_mao_dealer(cartas_dealer)
            jogador = mostrar_mao_jogador(cartas_jogador)
            
            if jogador >= 21 or acao[0] == 'd':
                break
            
            acao = acoes(creditos, aposta, cartas_jogador)
        
            while acao[0] == 'e':
                print('\nAção inválida')
                
                mostrar_mao_dealer(cartas_dealer)
                jogador = mostrar_mao_jogador(cartas_jogador)
                
                acao = acoes(creditos, aposta, cartas_jogador)
                
        if jogador > 21:
            
            print('\nBusted!')
            
            win = False
            
        else:
            
            soma_dealer = sum(cartas_dealer.values())
            
            while soma_dealer < 17:
                nova_carta_dealer = tirar_carta(cartas)
                
                cartas_dealer[nova_carta_dealer[0]] = nova_carta_dealer[1]
                
                soma_dealer += nova_carta_dealer[1]
                
                if 1 in cartas_dealer.values() and soma_dealer <= 11 and soma_dealer + 10 >= 17:
                        As = True
                        
                        break
                
                else:
                    As = False
                    
                
            mostrar_mao_dealer(cartas_dealer)
            jogador = mostrar_mao_jogador(cartas_jogador)
            
            if 1 in cartas_jogador.values() and jogador <= 11:
                jogador += 10
                
            if As == True:
                soma_dealer += 10
            
            if soma_dealer > 21 or jogador > soma_dealer:
                win = True
                
            elif soma_dealer > jogador:
                win = False
                
            else:
                win = None
        
    if win == True:
        
        print('\nPlayer win!')
        
        
    if win == False:
        
        print('\nDealer win!')
        
        aposta = -(aposta)
        
    if win == None:
        
        print('\nPush')
        
        aposta = 0
        
    creditos += aposta
    
    return creditos
     
def main():
    start = input('\nBLACKJACK\n\nPrecione Enter para começar ')

    creditos = 100

    if start == '':
        while True:
            
            if creditos < 5:
                
                print('\nSaldo insuficiente. Fim de jogo')
                
                break
            
            creditos = blackjack(creditos)
                
            start = input('\nPrecione Enter para continuar\n')
                    
            if start != '':
                break
            
if __name__ == "__main__":
    main()
