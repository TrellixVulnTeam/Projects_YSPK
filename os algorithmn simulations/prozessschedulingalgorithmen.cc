/*
Used Compiler:  g++ -std=c++17 -Wall -o prozessschedulingalgorithmen prozessschedulingalgorithmen.cc
Folgen:
5|3|12|100|1|2|3|4|5|	
5|4|3|2|1|100|12|3|5|
23|17|31|29|71|2|5|113|
*/
#include<iostream>
#include<vector>
#include<string>
#include<map>
#include<algorithm>
using namespace std;

void FCFS(vector<int> runtime)
{
	int awt = 0;
	int timer[runtime.size()];
	bool marked[runtime.size()];
	
	for(unsigned int i = 0; i < runtime.size(); i++)
	{
		marked[i] = false;
		timer[i] = 0;
	}	
	
	cout << "First-Come-First-Served" << endl;
	cout << endl;
	for(unsigned int i = 0; i < runtime.size(); i++)
	{
		marked[i] = true;
		for(unsigned int k = 0; k < runtime.size(); k++)
		{
			if(!marked[k])
			{
				timer[k]+= runtime[i];
			}
		}	
		cout << "Process: " << i << " ti: " << runtime[i] << endl;
	}
	
	for(unsigned int i = 0; i < runtime.size(); i++)
	{
		awt += timer[i]+runtime[i];
	}
	cout << endl;
	cout << "Turn-around-time: " << awt << endl;
}

void SJF(vector<int> runtime)
{
	map<int, int> SJF_runtime;
	int awt = 0;
	int timer[runtime.size()];
	bool marked[runtime.size()];
	
	for(unsigned int i = 0; i < runtime.size(); i++)
	{
		marked[i] = false;
		timer[i] = 0;
	}	
	
	cout << "Shortest-Job-First" << endl;
	cout << endl;
	for(unsigned int i = 0; i < runtime.size(); i++)
	{
		SJF_runtime.insert(make_pair(runtime[i]*100+i, i));
	}
	
	map<int, int>::iterator it = SJF_runtime.begin();
	while(it != SJF_runtime.end())
	{
		cout << "Process: " << it->second << " ti: " << runtime[it->second] << endl;
		marked[it->second] = true;
		for(unsigned int i = 0; i < runtime.size(); i++)
		{
			if(!marked[i])
			{
				timer[i] += runtime[it->second];
			}
		}
		it++;
	}
	
	for(unsigned int i = 0; i < runtime.size(); i++)
	{
		awt += timer[i]+runtime[i];
	}
	cout << endl;
	cout << "Turn-around-time: " << awt << endl;
}	

void SRTF(vector<int> runtime)
{
	/*Dieses Verfahren SRTF kommt nur dann zum tragn wenn, während ein prozess
	bereits läuft ein neuer prozess dazu kommt. dies ist in dieser Aufgabe nicht gegeben
	deshalb entspricht SRTF dem SJF*/
	map<int, int> SJF_runtime;
	int awt = 0;
	int timer[runtime.size()];
	bool marked[runtime.size()];
	
	for(unsigned int i = 0; i < runtime.size(); i++)
	{
		marked[i] = false;
		timer[i] = 0;
	}	
	
	cout << "Shortest-Remaining-Time-First" << endl;
	cout << endl;
	for(unsigned int i = 0; i < runtime.size(); i++)
	{
		SJF_runtime.insert(make_pair(runtime[i]*100+i, i));
	}
	
	map<int, int>::iterator it = SJF_runtime.begin();
	while(it != SJF_runtime.end())
	{
		cout << "Process: " << it->second << " ti: " << runtime[it->second] << endl;
		marked[it->second] = true;
		for(unsigned int i = 0; i < runtime.size(); i++)
		{
			if(!marked[i])
			{
				timer[i] += runtime[it->second];
			}
		}
		it++;
	}
	
	for(unsigned int i = 0; i < runtime.size(); i++)
	{
		awt += timer[i]+runtime[i];
	}
	cout << endl;
	cout << "Turn-around-time: " << awt << endl;
}

void RoundRobin(vector<int> runtime, int quantum)
{
	int awt = 0, ti = 0, lauf = 0;
	unsigned int counter = 0;
	bool again = true;
	int timer[runtime.size()];
	bool marked[runtime.size()];
	bool inprocess[runtime.size()];
	
	for(unsigned int i = 0; i < runtime.size(); i++)
	{
		inprocess[i] = false;
		marked[i] = false;
		timer[i] = 0;
	}
	
	cout << "Round-Robin" << endl;
	cout << endl;
	while(again)
	{
		for(unsigned int i = 0; i < runtime.size(); i++)
		{
			if(!marked[i])
			{
				if(runtime[i] > 0)
				{
					if(runtime[i] < quantum)
					{
						ti = runtime[i];
					}	
					else
					{
						ti = quantum;
					}
					lauf += ti;
					cout << "Process: " << i << " ti: " << ti << endl;
				}
				
				inprocess[i] = true;
					
				for(unsigned int k = 0; k < runtime.size(); k++)
				{
					if(!inprocess[k] && !marked[k])
					{
						timer[k]+= min(runtime[i], quantum);
					}
						
				}
				
				if(runtime[i] > quantum)
				{
					runtime[i]-= quantum;
				}
				else
				{
					runtime[i] = 0;
					marked[i] = true;
				}	
				inprocess[i] = false;
			}
		}
		for(unsigned int i = 0; i < runtime.size(); i++)
		{
			if(marked[i])
			{
				counter++;
			}
		}
		if(counter == runtime.size())
		{
			again = false;
		}
		else
		{
			counter = 0;
		}
	}
	
	for(unsigned int i = 0; i < runtime.size(); i++)
	{
		awt += timer[i];
	}

	awt += lauf;
	cout << endl;
	cout << "Turn-around-time: " << awt << endl;
}										
					
int main(int argc, char *argv[])
{
	vector<int> runtime_array;
	int quantum = 0;
	string input, temp;
	
	quantum = stoi(argv[1]);
	cout << "Prozessschedulingalgorithmen Simuation 1.0" << endl;
	
	cout << "Please enter the runtime value-serie: " << flush;
	cin >> input;
	
	for(unsigned int i = 0; i < input.length(); i++)
	{
		if(input[i] == '|')
		{
			runtime_array.push_back(stoi(temp));
			temp = "";
		}
		else
		{
			temp+= input[i];
		}	
	}
	
	cout << "--------------------------------------------" << endl;
	FCFS(runtime_array);
	cout << "--------------------------------------------" << endl;
	SJF(runtime_array);
	cout << "--------------------------------------------" << endl;
	SRTF(runtime_array);
	cout << "--------------------------------------------" << endl;
	RoundRobin(runtime_array, quantum);
	
	return 0;
}
	
  
				