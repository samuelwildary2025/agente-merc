#!/usr/bin/env python3
"""
Teste de temperatura corrigido para GPT-5-mini
Verifica se o modelo funciona sem o parâmetro temperature
"""
import os
import sys
from langchain_openai import ChatOpenAI

def test_gpt5_mini_sem_temperatura():
    """Testa GPT-5-mini sem parâmetro temperature"""
    
    openai_api_key = os.getenv('OPENAI_API_KEY', 'your-openai-api-key-here')
    
    if openai_api_key == 'your-openai-api-key-here':
        print("⚠️  WARNING: Usando API key de placeholder")
        print("💡 Para testar real, configure: export OPENAI_API_KEY='sua-api-key'")
        return False
    
    try:
        print("🧪 Testando GPT-5-mini SEM parâmetro temperature...")
        
        # Testar exatamente como está no código corrigido
        llm = ChatOpenAI(
            model="gpt-5-mini",
            openai_api_key=openai_api_key
            # temperature REMOVIDO para GPT-5-mini
        )
        
        test_message = "Olá, qual é o seu nome?"
        response = llm.invoke(test_message)
        
        print("✅ SUCESSO: GPT-5-mini funcionou sem temperature!")
        print(f"📨 Resposta: {response.content[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ ERRO: {str(e)}")
        if "temperature" in str(e).lower():
            print("🔧 Ainda há problema com temperature")
        elif "gpt-5-mini" in str(e).lower():
            print("🔧 Pode ser problema de modelo ou API key")
        return False

def test_outros_modelos_com_temperatura():
    """Testa se outros modelos ainda funcionam com temperature"""
    
    openai_api_key = os.getenv('OPENAI_API_KEY', 'your-openai-api-key-here')
    
    if openai_api_key == 'your-openai-api-key-here':
        return False
    
    try:
        print("🧪 Testando gpt-4o-mini COM temperature...")
        
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            openai_api_key=openai_api_key,
            temperature=0.7  # Deve funcionar
        )
        
        test_message = "Oi, tudo bem?"
        response = llm.invoke(test_message)
        
        print("✅ SUCESSO: gpt-4o-mini funcionou com temperature!")
        return True
        
    except Exception as e:
        print(f"❌ ERRO gpt-4o-mini: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Teste de Correção de Temperatura para GPT-5-mini")
    print("=" * 60)
    
    success1 = test_gpt5_mini_sem_temperatura()
    success2 = test_outros_modelos_com_temperatura()
    
    print("\n" + "=" * 60)
    print("📊 RESULTADOS:")
    print(f"GPT-5-mini sem temperature: {'✅ OK' if success1 else '❌ FALHOU'}")
    print(f"gpt-4o-mini com temperature: {'✅ OK' if success2 else '❌ FALHOU'}")
    
    if success1:
        print("\n🎉 Correção aplicada com sucesso!")
        print("GPT-5-mini agora funciona sem parâmetro temperature")
    else:
        print("\n⚠️  Teste falhou - verifique sua API key real")