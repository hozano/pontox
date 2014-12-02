#include <iostream>
#include <string>
#include<exception>
using namespace std;

class DepositoException:public exception{
public:
    virtual const string what(){return "Deposito Inválido";}
};
class SaqueException:public exception{
public:
	virtual const string what(){return "Saque Inválido";};
};

class Conta{
protected:
    string cod;
    float saldo;
public:
    Conta(string _cod, float _saldo){cod = _cod; saldo = _saldo;}
    string getCod(){return cod;}
    float getSaldo(){return saldo;}
    void depositar(float valor){
        if(valor < 1) throw DepositoException();
        else saldo += valor;
    }
    virtual void sacar(float valor) = 0;
};
class ContaCorrente:public Conta{
private:
    float taxas;
public:
    ContaCorrente(string cod, float saldo) : Conta(cod,saldo){
        taxas = 0;
    }
    void sacar(float valor){
    	if(valor > saldo){
    		if(valor - saldo < 201){saldo -= valor;}
    		else throw SaqueException();
    	}
    	else saldo -= valor;
    }
};

template<class Abstract> class ArrayList{
private:
	Abstract * array;
	int tamanho;
	int index;
public:
	ArrayList(){index = 0 ;tamanho = 5; array = new  Abstract[tamanho];}
	void aumentar(){
		Abstract * temp = new  Abstract[tamanho + 10];
		for (int i = 0; i < tamanho; ++i){
			temp[i] = array[i];
		}
		delete array;
		array = temp;
		tamanho += 10;
	}
	void inserir(Abstract valor){
		if(index==tamanho){
			aumentar();
		}
		array[index] = valor;
		index++;
	}
};
class Banco{
private:
	ArrayList<ContaCorrente> arrayContas;
public:
	void inserirConta(ContaCorrente conta){
		arrayContas.inserir(conta);
	}
};

int main(void) {
    Banco banco();
    ContaCorrente conta("12321",521.5);

    banco.inserirConta(conta);
}