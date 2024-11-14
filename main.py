#Importações SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import date
from getpass import getpass

#Criação de engine para banco de dados SQLite e configuração da sessão
db = create_engine('sqlite:///banco_restaurante.db', echo=False)
Session = sessionmaker(bind=db)
session = Session()

#Classe base para definir as tabelas do banco de dados com SQLAlchemy
Base = declarative_base()

# Controle de acesso
USUARIOS = {
    "admin": "admin123",
    "gerente": "gerente123"
}

def autenticar_usuario():
    print("=== Autenticação ===")
    usuario = input("Usuário: ")
    senha = getpass("Senha: ")

    if USUARIOS.get(usuario) == senha:
        print("Acesso permitido")
        return True
    else:
        print("Acesso negado, usuário ou senha incorretos")
        return False

#Definicao das entidades do banco de dados

class Categoria(Base):
    __tablename__ = 'categorias'

    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    nome_categoria = Column(String, nullable=False)
    
    pratos = relationship("Prato", back_populates="categoria")
    
    def __repr__(self):
        return f"<Categoria(id={self.id_categoria}, nome={self.nome_categoria})>"

class Prato(Base):
    __tablename__ = 'pratos'

    id_prato = Column(Integer, primary_key=True, autoincrement=True)
    nome_prato = Column(String, nullable=False)
    preco = Column(Integer, nullable=False)
    id_categoria = Column(Integer, ForeignKey('categorias.id_categoria'))

    categoria = relationship("Categoria", back_populates="pratos")

    def __repr__(self):
        return f"<Prato(id={self.id_prato}, nome={self.nome_prato}, preco={self.preco})>"

class Cliente(Base):
    __tablename__ = 'clientes'

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nome_cliente = Column(String, nullable=False)
    telefone = Column(String, nullable=False)

    def __repr__(self):
        return f"<Cliente(id={self.id_cliente}, nome={self.nome_cliente}, telefone={self.telefone})>"

class Pedido(Base):
    __tablename__ = 'pedidos'

    id_pedido = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente'))
    id_prato = Column(Integer, ForeignKey('pratos.id_prato'))
    data_pedido = Column(Date)

    cliente = relationship("Cliente")
    prato = relationship("Prato")

    def __repr__(self):
        return f"<Pedido(id={self.id_pedido}, cliente={self.id_cliente}, prato={self.id_prato}, data={self.data_pedido})>"

#Criação das tabelas no banco de dados
Base.metadata.create_all(bind=db)

#Operações CRUD (Create, Read, Update, Delete)

#Criar

def criar_categoria(nome_categoria):
    with Session() as session:
        nova_categoria = Categoria(nome_categoria=nome_categoria)
        session.add(nova_categoria)
        try:
            session.commit()
            print("Categoria criada com sucesso!")
        except Exception as e:
            session.rollback()
            print(f"Erro ao criar categoria: {e}")

def criar_prato(nome_prato, preco, id_categoria):
    with Session() as session:
        # Verificar se a categoria existe
        categoria = session.query(Categoria).filter(Categoria.id_categoria == id_categoria).first()
        if categoria:
            novo_prato = Prato(nome_prato=nome_prato, preco=preco, id_categoria=id_categoria)
            session.add(novo_prato)
            try:
                session.commit()
                print(f"Prato '{nome_prato}' criado com sucesso!")
            except Exception as e:
                session.rollback()
                print(f"Erro ao criar prato: {e}")
        else:
            print(f"Categoria com ID {id_categoria} não encontrada. Não é possível criar o prato.")

def criar_cliente(nome_cliente, telefone):
     with Session() as session:
        novo_cliente = Cliente(nome_cliente=nome_cliente, telefone=telefone)
        session.add(novo_cliente)
        try:
            session.commit()
            print("Cliente criado com sucesso!")
            return novo_cliente
        except Exception as e:
            session.rollback()
            print(f"Erro ao criar cliente: {e}")

def criar_pedido(id_cliente, id_prato, data_pedido):
    with Session() as session:
        # Verificar se o cliente existe
        cliente = session.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()
        if cliente:
            prato = session.query(Prato).filter(Prato.id_prato == id_prato).first()
            if prato:
                novo_pedido = Pedido(id_cliente=id_cliente, id_prato=id_prato, data_pedido=data_pedido)
                session.add(novo_pedido)
                try:
                    session.commit()
                    print(f"Pedido criado com sucesso!")
                except Exception as e:
                    session.rollback()
                    print(f"Erro ao criar pedido: {e}")
            else:
                print(f"Prato com ID {id_prato} não encontrado.")
        else:
            print(f"Cliente com ID {id_cliente} não encontrado.")


#Ler um registro pela ID

def ler_categoria(id_categoria):
    with Session() as session:
        try:
            categoria = session.query(Categoria).filter_by(id_categoria=id_categoria).first()
            return categoria
        except Exception as e:
            print(f"Erro ao ler categoria: {e}")

def ler_prato(id_prato):
    with Session() as session:
        try:
            prato = session.query(Prato).filter_by(id_prato=id_prato).first()
            return prato
        except Exception as e:
            print(f"Erro ao ler prato: {e}")

def ler_cliente(id_cliente):
    with Session() as session:
        try:
            cliente = session.query(Cliente).filter_by(id_cliente=id_cliente).first()
            return cliente
        except Exception as e:
            print(f"Erro ao ler cliente: {e}")

def ler_pedido(id_pedido):
    with Session() as session:
        try:
            pedido = session.query(Pedido).filter_by(id_pedido=id_pedido).first()
            return pedido
        except Exception as e:
            print(f"Erro ao ler pedido: {e}")

#Ler todos os registros
#Exemplo de print:
#clientes =ler_todos_clientes()
#for cliente in clientes:
    #print(cliente)

def ler_todos_clientes():
    with Session() as session:
        return session.query(Cliente).all()

def ler_todos_pratos():
    with Session() as session:
        return session.query(Prato).all()

def ler_todas_categorias():
    with Session() as session:
        return session.query(Categoria).all()

def ler_todos_pedidos():
    with Session() as session:
        return session.query(Pedido).all()

#Atualizar

def atualizar_categoria(id_categoria, nome_categoria):
    with Session() as session:
        try:
            categoria = session.query(Categoria).filter_by(id_categoria=id_categoria).first()
            if categoria:
                categoria.nome_categoria = nome_categoria
                session.commit()
                print("Categoria atualizada com sucesso!")
            return categoria
        except Exception as e:
            session.rollback()
            print(f"Erro ao atualizar categoria: {e}")

def atualizar_prato(id_prato, nome_prato=None, preco=None, id_categoria=None):
    with Session() as session:
        try:
            prato = session.query(Prato).filter_by(id_prato=id_prato).first()
            if prato:
                if nome_prato is not None:
                    prato.nome_prato = nome_prato
                if preco is not None:
                    prato.preco = preco
                if id_categoria is not None:
                    prato.id_categoria = id_categoria
                session.commit()
            return prato
        except Exception as e:
            session.rollback()
            print(f"Erro ao atualizar prato: {e}")

def atualizar_cliente(id_cliente, nome_cliente=None, telefone=None):
    with Session() as session:
        try:
            cliente = session.query(Cliente).filter_by(id_cliente=id_cliente).first()
            if cliente:
                if nome_cliente is not None:
                    cliente.nome_cliente = nome_cliente
                if telefone is not None:
                    cliente.telefone = telefone
                session.commit()
            return cliente
        except Exception as e:
            session.rollback()
            print(f"Erro ao atualizar cliente: {e}")

def atualizar_pedido(id_pedido, id_cliente=None, id_prato=None, data_pedido=None):
    with Session() as session:
        try:
            pedido = session.query(Pedido).filter_by(id_pedido=id_pedido).first()
            if pedido:
                if id_cliente is not None:
                    pedido.id_cliente = id_cliente
                if id_prato is not None:
                    pedido.id_prato = id_prato
                if data_pedido is not None:
                    pedido.data_pedido = data_pedido
                session.commit()
            return pedido
        except Exception as e:
            session.rollback()
            print(f"Erro ao atualizar pedido: {e}")

#Excluir

def excluir_categoria(id_categoria):
    with Session() as session:
        try:
            categoria = session.query(Categoria).filter_by(id_categoria=id_categoria).first()
            if categoria:
                session.delete(categoria)
                session.commit()
                print(f"Categoria {id_categoria} excluída com sucesso.")
            else:
                print(f"Categoria com ID {id_categoria} não encontrada.")
        except Exception as e:
            session.rollback()
            print(f"Erro ao excluir categoria: {e}")

def excluir_prato(id_prato):
    with Session() as session:
        try:
            prato = session.query(Prato).filter_by(id_prato=id_prato).first()
            if prato:
                session.delete(prato)
                session.commit()
                print(f"Prato {id_prato} excluído com sucesso.")
            else:
                print(f"Prato com ID {id_prato} não encontrado.")
        except Exception as e:
            session.rollback()
            print(f"Erro ao excluir prato: {e}")

def excluir_cliente(id_cliente):
    with Session() as session:
        try:
            cliente = session.query(Cliente).filter_by(id_cliente=id_cliente).first()
            if cliente:
                session.delete(cliente)
                session.commit()
                print(f"Cliente {id_cliente} excluído com sucesso.")
            else:
                print(f"Cliente com ID {id_cliente} não encontrado.")
        except Exception as e:
            session.rollback()
            print(f"Erro ao excluir cliente: {e}")

def excluir_pedido(id_pedido):
    with Session() as session:
        try:
            pedido = session.query(Pedido).filter_by(id_pedido=id_pedido).first()
            if pedido:
                session.delete(pedido)
                session.commit()
                print(f"Pedido {id_pedido} excluído com sucesso.")
            else:
                print(f"Pedido com ID {id_pedido} não encontrado.")
        except Exception as e:
            session.rollback()
            print(f"Erro ao excluir pedido: {e}")

#Função para consultar todas as tabelas

def consultar_todas_tabelas():
    with Session() as session:
        print("Categorias:")
        categorias = session.query(Categoria).all()
        if categorias:
            for categoria in categorias:
                print(f"{categoria}")
        else:
            print("Nenhuma categoria cadastrada.")

        print("Pratos:")
        pratos = session.query(Prato).all()
        if pratos:
            for prato in pratos:
                print(f"{prato}")
        else:
            print("Nenhum prato cadastrado.")

        print("Clientes:")
        clientes = session.query(Cliente).all()
        if clientes:
            for cliente in clientes:
                print(f"{cliente}")
        else:
            print("Nenhum cliente cadastrado.")

        print("Pedidos:")
        pedidos = session.query(Pedido).join(Cliente).join(Prato).all()
        if pedidos:
            for pedido in pedidos:
                print(f"Pedido {pedido.id_pedido}: Cliente {pedido.cliente.nome_cliente}, "
                      f"Prato {pedido.prato.nome_prato}, Data {pedido.data_pedido}")
        else:
            print("Nenhum pedido cadastrado.")

#Álgebra relacional

def selecionar_pratos_por_preco(preco_minimo):
    with Session() as session:
        try:
            pratos = session.query(Prato).filter(Prato.preco >= preco_minimo).all()
            for prato in pratos:
                print(f"{prato}")
        except Exception as e:
            print(f"Erro ao selecionar pratos por preço: {e}")

def projetar_clientes_nome_telefone():
    with Session() as session:
        try:
            clientes = session.query(Cliente.nome_cliente, Cliente.telefone).all()
            for cliente in clientes:
                print(f"Nome: {cliente.nome_cliente}, Telefone: {cliente.telefone}")
        except Exception as e:
            print(f"Erro ao projetar nome e telefone dos clientes: {e}")

def uniao_pratos_categoria(preco_minimo):
    with Session() as session:
        try:
            pratos = session.query(Prato).filter(Prato.preco >= preco_minimo).all()
            categorias = session.query(Categoria).all()

            # Exibindo pratos e categorias juntos (exemplo de união simples)
            for prato in pratos:
                print(f"Prato: {prato.nome_prato}, Preço: {prato.preco}")
            for categoria in categorias:
                print(f"Categoria: {categoria.nome_categoria}")
        except Exception as e:
            print(f"Erro ao realizar união entre pratos e categorias: {e}")

def junção_clientes_pedidos():
    with Session() as session:
        try:
            pedidos = session.query(Pedido, Cliente, Prato).join(Cliente).join(Prato).all()
            for pedido, cliente, prato in pedidos:
                print(f"Pedido {pedido.id_pedido}: Cliente {cliente.nome_cliente}, "
                      f"Prato {prato.nome_prato}, Data {pedido.data_pedido}")
        except Exception as e:
            print(f"Erro ao realizar junção entre clientes e pedidos: {e}")

def diferença_pratos_nao_pedidos():
    with Session() as session:
        try:
            pratos = session.query(Prato).all()
            pedidos = session.query(Pedido).all()

            # Criar uma lista de IDs de pratos que já foram pedidos
            pratos_pedidos = [pedido.id_prato for pedido in pedidos]

            # Filtrar os pratos que não estão nos pedidos
            pratos_nao_pedidos = [prato for prato in pratos if prato.id_prato not in pratos_pedidos]

            for prato in pratos_nao_pedidos:
                print(f"Prato não pedido: {prato.nome_prato}")
        except Exception as e:
            print(f"Erro ao selecionar pratos não pedidos: {e}")



#Funções para definir os menus para o usuário

def exibir_menu():
    print("--- MENU PRINCIPAL ---")
    print("1. Categorias")
    print("2. Pratos")
    print("3. Clientes")
    print("4. Pedidos")
    print("5. Consultar todas as tabelas")
    print("6. Operações de álgebra relacional")
    print("0. Sair")
    opcao = input("Escolha uma opção: ")
    return opcao

def menu_categoria():
    print("--- MENU CATEGORIAS ---")
    print("1. Criar categoria")
    print("2. Ler categoria")
    print("3. Atualizar categoria")
    print("4. Excluir categoria")
    opcao = input("Escolha uma opção: ")
    return opcao

def menu_prato():
    print("--- MENU PRATOS ---")
    print("1. Criar prato")
    print("2. Ler prato")
    print("3. Atualizar prato")
    print("4. Excluir prato")
    opcao = input("Escolha uma opção: ")
    return opcao

def menu_cliente():
    print("--- MENU CLIENTES ---")
    print("1. Criar cliente")
    print("2. Ler cliente")
    print("3. Atualizar cliente")
    print("4. Excluir cliente")
    opcao = input("Escolha uma opção: ")
    return opcao

def menu_pedido():
    print("--- MENU PEDIDOS ---")
    print("1. Criar pedido")
    print("2. Ler pedido")
    print("3. Atualizar pedido")
    print("4. Excluir pedido")
    opcao = input("Escolha uma opção: ")
    return opcao

def menu_algebra_relacional():
    print("--- MENU ÁLGEBRA RELACIONAL ---")
    print("1. Selecionar pratos por preço")
    print("2. Projeção de clientes (nome e telefone)")
    print("3. Junção de clientes e pedidos")
    print("4. Diferença de pratos não pedidos")
    opcao = input("Escolha uma operação: ")
    return opcao

#Função para o menu principal

def main():
    if not autenticar_usuario():
        print("Encerrando o programa devido a falha na autenticação.")
        return
    
    while True:
        opcao = exibir_menu()

        if opcao == '1': #Categorias
            escolha = menu_categoria()
            if escolha == '1': #Criar categoria
                nome_categoria = input("Digite o nome da nova categoria: ")
                criar_categoria(nome_categoria)
                print("Categoria criada com sucesso!")
            elif escolha == '2': #Ler categoria
                id_categoria = input("Digite o ID da categoria: ")
                categoria = ler_categoria(int(id_categoria))
                print(categoria)
            elif escolha == '3': #Atualizar categoria
                id_categoria = input("Digite o ID da categoria a ser atualizada: ")
                nome_categoria = input("Digite o novo nome da categoria: ")
                atualizar_categoria(int(id_categoria), nome_categoria)
                print("Categoria atualizada com sucesso!")
            elif escolha == '4': #Excluir categoria
                id_categoria = input("Digite o ID da categoria: ")
                if id_categoria.isdigit():
                    excluir_categoria(int(id_categoria))
                else:
                    print("ID inválido. Por favor, insira um número inteiro.")
        
        elif opcao == '2': #Pratos
            escolha = menu_prato()
            if escolha == '1': #Criar prato
                nome_prato = input("Digite o nome do novo prato: ")
                preco = input("Digite o preço do prato: ")
                id_categoria = input("Digite o ID da categoria do prato: ")
                criar_prato(nome_prato, int(preco), int(id_categoria))
                print("Prato criado com sucesso!")
            elif escolha == '2': #Ler prato
                id_prato = input("Digite o ID do prato: ")
                prato = ler_prato(int(id_prato))
                print(prato)
            elif escolha == '3': #Atualizar prato
                id_prato = input("Digite o ID do prato a ser atualizado: ")
                nome_prato = input("Digite o novo nome do prato (ou deixe vazio para não alterar): ")
                preco = input("Digite o novo preço do prato (ou deixe vazio para não alterar): ")
                id_categoria = input("Digite o novo ID da categoria (ou deixe vazio para não alterar): ")
                atualizar_prato(
                    int(id_prato),
                    nome_prato if nome_prato else None,
                    int(preco) if preco else None,
                    int(id_categoria) if id_categoria else None
                )
                print("Prato atualizado com sucesso!")
            elif escolha == '4': #Excluir prato
                id_prato = input("Digite o ID do prato: ")
                if id_prato.isdigit():
                    excluir_prato(int(id_prato))
                else:
                    print("ID inválido. Por favor, insira um número inteiro.")

        elif opcao == '3': #Clientes
            escolha = menu_cliente()
            if escolha == '1': #Criar cliente
                nome_cliente = input("Digite o nome do novo cliente: ")
                telefone = input("Digite o telefone do cliente: ")
                criar_cliente(nome_cliente, telefone)
                print("Cliente criado com sucesso!")
            elif escolha == '2': #Ler cliente
                id_cliente = input("Digite o ID do cliente: ")
                cliente = ler_cliente(int(id_cliente))
                print(cliente)
            elif escolha == '3': #Atualizar cliente
                id_cliente = input("Digite o ID do cliente a ser atualizado: ")
                nome_cliente = input("Digite o novo nome do cliente (ou deixe vazio para não alterar): ")
                telefone = input("Digite o novo telefone do cliente (ou deixe vazio para não alterar): ")
                atualizar_cliente(
                    int(id_cliente),
                    nome_cliente if nome_cliente else None,
                    telefone if telefone else None
                )
                print("Cliente atualizado com sucesso!")
            elif escolha == '4': #Excluir cliente
                id_cliente = input("Digite o ID do cliente: ")
                if id_cliente.isdigit():
                    excluir_cliente(int(id_cliente))
                else:
                    print("ID inválido. Por favor, insira um número inteiro.")

        elif opcao == '4': #Pedidos
            escolha = menu_pedido()
            if escolha == '1': #Criar pedido
                id_cliente = input("Digite o ID do cliente: ")
                id_prato = input("Digite o ID do prato: ")
                data_pedido = input("Digite a data do pedido (AAAA-MM-DD): ")
                criar_pedido(int(id_cliente), int(id_prato), date.fromisoformat(data_pedido))
                print("Pedido criado com sucesso!")
            elif escolha == '2': #Ler pedido
                id_pedido = input("Digite o ID do pedido: ")
                pedido = ler_pedido(int(id_pedido))
                print(pedido)
            elif escolha == '3': #Atualizar pedido
                id_pedido = input("Digite o ID do pedido a ser atualizado: ")
                id_cliente = input("Digite o novo ID do cliente (ou deixe vazio para não alterar): ")
                id_prato = input("Digite o novo ID do prato (ou deixe vazio para não alterar): ")
                data_pedido = input("Digite a nova data do pedido (AAAA-MM-DD) ou deixe vazio: ")
                atualizar_pedido(
                    int(id_pedido),
                    int(id_cliente) if id_cliente else None,
                    int(id_prato) if id_prato else None,
                    date.fromisoformat(data_pedido) if data_pedido else None
                )
                print("Pedido atualizado com sucesso!")
            elif escolha == '4': #Excluir pedido
                id_pedido = input("Digite o ID do pedido: ")
                if id_pedido.isdigit():
                    excluir_pedido(int(id_pedido))
                else:
                    print("ID inválido. Por favor, insira um número inteiro.")

        elif opcao == '5': #Consultar todas as tabelas
            consultar_todas_tabelas()
        
        elif opcao == '6':  # Operações de álgebra relacional
            operacao = menu_algebra_relacional()
            if operacao == '1':  # Seleção por preço
                preco = float(input("Digite o preço mínimo: "))
                selecionar_pratos_por_preco(preco)
            elif operacao == '2':  # Projeção de clientes
                projetar_clientes_nome_telefone()
            elif operacao == '3':  # Junção de clientes e pedidos
                junção_clientes_pedidos()
            elif operacao == '4':  # Diferença de pratos não pedidos
                diferença_pratos_nao_pedidos()

        elif opcao == '0': #Sair
            print("Saindo")
            break

        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

#Executa o menu principal
main()