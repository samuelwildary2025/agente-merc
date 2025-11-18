#!/usr/bin/env python3
"""
Teste de temperatura para GPT-5-mini
Verifica se o modelo aceita diferentes valores de temperatura
"""
import os
import sys
from langchain_openai import ChatOpenAI

def test_temperature(temperature):
    """Testa GPT-5-mini com uma temperatura específica"""
    
    openai_api_key = os.getenv('OPENAI_API_KEY', 'your-openai-api-key-here')
    
    if openai_api_key == 'your-openai-api-key-here':
        print("⚠️  WARNING: Usando API key de placeholder")
        return False
    
    try:
        print(f"🧪 Testando GPT-5-mini com temperatura {temperature}...")
        
        llm = ChatOpenAI(
            model="gpt-5-mini",
            openai_api_key=openai_api_key,
            temperature=temperature
        )
        
        test_message = "Oi, tudo bem?"
        response = llm.invoke(test_message)
        
        print(f"✅ SUCESSO: Temperatura {temperature} funcionou!")
        print(f"📨 Resposta: {response.content[:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ ERRO com temperatura {temperature}: {str(e)}")
        if "temperature" in str(e).lower():
            print(f"🔧 Parece haver um problema específico com temperatura {temperature}")
        return False

def test_faixa_temperatura():
    """Testa diferentes valores de temperatura"""
    
    print("🌡️  Testando faixa de temperatura para GPT-5-mini")
    print("=" * 60)
    
    # Testar valores comuns de temperatura
    temperaturas = [0.0, 0.3, 0.5, 0.7, 1.0, 1.2, 1.5, 2.0]
    
    resultados = {}
    
    for temp in temperaturas:
        resultados[temp] = test_temperature(temp)
        print()  # Linha em branco entre testes
    
    print("📊 RESUMO DOS TESTES:")
    print("=" * 60)
    for temp, sucesso in resultados.items():
        status = "✅ OK" if sucesso else "❌ FALHOU"
        print(f"Temperatura {temp}: {status}")
    
    # Identificar padrão
    temperaturas_ok = [temp for temp, sucesso in resultados.items() if sucesso]
    if temperaturas_ok:
        print(f"\n🎯 Temperaturas que funcionam: {temperaturas_ok}")
    else:
        print("\n⚠️  Nenhuma temperatura funcionou com API key de placeholder")

if __name__ == "__main__":
    test_faixa_temperatura()