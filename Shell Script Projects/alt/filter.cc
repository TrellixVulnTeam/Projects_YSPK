#include<iostream>
#include <fstream>
#include<string>

int main(int argc, char *argv[])
{
	string filePath = "/home/philipp/Schreibtisch/test.txt";
	string line;
	
	ifstream myfile (filePath);
	
	if (myfile.is_open())
 	{
    	while(getline(myfile,line))
    	{
      	cout << line << '\n';
    	}
    	myfile.close();
  	}
  	else
  	{
		cout << "Unable to open file"; 
  	}
	
  	return 0;
}