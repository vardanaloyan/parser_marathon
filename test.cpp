#include<iostream>
using namespace std;

int fib(int N)
{
	if (N==1)
	{
		return 0;
	}
	if (N==2)
	{
		return 1;
	}
	return fib(N-1)+fib(N-2);

}

int main()
{
	for(int n=1;n<=10;n++)
		cout<<fib(n)<<",";
		cout<<endl;
	

	return 0;
}