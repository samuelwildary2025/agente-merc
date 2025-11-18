#!/usr/bin/env python3
"""
Teste de verificação do sistema de memória do agente
Verifica como o PostgreSQL está armazenando e recuperando mensagens
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from memory.limited_postgres_memory import LimitedPostgresChatMessageHistory
from config.settings import settings
from langchain_core.messages import HumanMessage, AIMessage

def test_memory_system():
    """Testa o sistema de memória completo"""
    
    print("🧪 Testando Sistema de Memória do Agente")
    print("=" * 60)
    
    # Testar com um session_id de exemplo
    session_id = "teste_memory_5585999999999"
    
    try:
        # Criar histórico de memória
        print(f"📁 Criando histórico para session_id: {session_id}")
        memory = LimitedPostgresChatMessageHistory(
            session_id=session_id,
            connection_string=settings.postgres_connection_string,
            table_name=settings.postgres_table_name,
            max_messages=settings.postgres_message_limit
        )
        
        # Verificar informações da sessão
        info = memory.get_session_info()
        print(f"📊 Info da sessão: {info}")
        
        # Adicionar algumas mensagens de teste
        print("\n💬 Adicionando mensagens de teste...")
        
        # Mensagem do cliente
        msg1 = HumanMessage(content="Quero um pacote de arroz")
        memory.add_message(msg1)
        print(f"✅ Adicionada: {msg1.content}")
        
        # Resposta do agente
        msg2 = AIMessage(content="Tem arroz 5kg R$18,90. Confirma?")
        memory.add_message(msg2)
        print(f"✅ Adicionada: {msg2.content}")
        
        # Outra mensagem do cliente
        msg3 = HumanMessage(content="Quero também feijão")
        memory.add_message(msg3)
        print(f"✅ Adicionada: {msg3.content}")
        
        # Verificar contagem
        count = memory.get_message_count()
        print(f"\n📈 Total de mensagens armazenadas: {count}")
        
        # Recuperar mensagens (com limite)
        print(f"\n🔍 Recuperando mensagens (limite: {settings.postgres_message_limit})...")
        messages = memory.messages
        print(f"📋 Mensagens recuperadas: {len(messages)}")
        
        for i, msg in enumerate(messages):
            msg_type = "🧑‍💼 Cliente" if isinstance(msg, HumanMessage) else "🤖 Agente"
            print(f"  {i+1}. {msg_type}: {msg.content[:50]}...")
        
        # Testar limpeza de contexto
        print(f"\n🧹 Testando detecção de confusão...")
        should_clear = memory.should_clear_context(messages)
        print(f"🤔 Deve limpar contexto? {should_clear}")
        
        # Testar com mensagens de confusão
        confused_messages = [
            HumanMessage(content="Quero produto"),
            AIMessage(content="Não consegui identificar o produto"),
            HumanMessage(content="O que você tem?"),
            AIMessage(content="Desculpe, não entendi. Pode informar o nome principal?")
        ]
        
        should_clear_confused = memory.should_clear_context(confused_messages)
        print(f"🤔 Com mensagens confusas, deve limpar? {should_clear_confused}")
        
        # Limpar tudo no final do teste
        print(f"\n🗑️  Limpando memória de teste...")
        memory.clear()
        final_count = memory.get_message_count()
        print(f"✅ Memória limpa! Mensagens restantes: {final_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de memória: {e}")
        return False

def verificar_configuracao_memoria():
    """Verifica configurações atuais de memória"""
    
    print("\n" + "=" * 60)
    print("🔧 Configuração Atual de Memória")
    print("=" * 60)
    
    print(f"📊 Limite de mensagens: {settings.postgres_message_limit}")
    print(f"🗄️  Tabela PostgreSQL: {settings.postgres_table_name}")
    print(f"🔗 String de conexão: {settings.postgres_connection_string[:50]}...")
    
    # Verificar se consegue conectar
    try:
        import psycopg2
        print("✅ psycopg2 disponível")
        
        # Testar conexão rápida
        conn = psycopg2.connect(settings.postgres_connection_string)
        cursor = conn.cursor()
        
        # Verificar se tabela existe
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = %s
            )
        """, (settings.postgres_table_name,))
        
        table_exists = cursor.fetchone()[0]
        print(f"📋 Tabela '{settings.postgres_table_name}' existe: {table_exists}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Problema com PostgreSQL: {e}")

if __name__ == "__main__":
    print("🚀 Teste Completo do Sistema de Memória")
    print("=" * 60)
    
    # Verificar configuração primeiro
    verificar_configuracao_memoria()
    
    # Testar sistema
    print("\n" + "=" * 60)
    success = test_memory_system()
    
    if success:
        print("\n🎉 Sistema de memória funcionando perfeitamente!")
    else:
        print("\n⚠️  Sistema de memória tem problemas para resolver.")