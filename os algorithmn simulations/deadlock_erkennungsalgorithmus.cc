#include<iostream>
#include<vector>
#include<string>
#include<fstream>
using namespace std;

bool vector_comparison_less_or_equal(vector<int> h, vector<int> g)
{
	// Function: Check if vector R[i] is less or equal to vector A
	//counter for succesfull checks and bool ckeck 
	int count = 0;
	bool check = false;
	//check if size of both vectors are equal
	if(h.size() == g.size())
	{
		for(int i = 0; i < h.size(); i++)
		{
			//check if h[i] is less or equal to g[i]
			if(h[i] <= g[i])
			{
				count++;
			}
		}
	}
	//check if counter is the same size as h.size()
	if(count == h.size())
	{
		check = true;
	}
	return check;
}	

int main(int argc, char *argv[])
{
	//Important Note: if you want to use an other txt file please change the layout to the given data files layout 
	//Define all variables
	int number_processes = 0, number_resource_variants = 0, value = 0;
	vector<vector<int> > C, R;
	vector<int> E, A;
	bool marked[number_processes];
	bool again = true;
	string filename, line, nextline, temp, logfilename;
	
	//read the given parameter into filename
	filename = argv[1];
	
	//read the complete data of filename into input
	ifstream input(filename);
	
	//error if data couldn't be read
	if (!input)
  	{
    	cerr << "Error can not open " << filename << "\n";
    	return 1;
  	}
	
	//read every line of input in line
	while(getline(input, line))
 	{
		if(line == "Log-file-Name:")
		{
			//get the nextline and store the value in logfilename
			getline(input, nextline);
			logfilename = nextline;
		}	
		else if(line == "Processes:")
		{
			//get the nextline and store the value in number_processes
			getline(input, nextline);
			number_processes = stoi(nextline);
		}
		else if(line == "Resource Variants:")
		{
			//get the nextline and store the value in number_resource_variants
			getline(input, nextline);
			number_resource_variants = stoi(nextline);
		}
		else if(line == "Number of resources per kind:")
		{
			//get the nextline and save it in nextline
			getline(input, nextline);
			//go through nextline 
			for(int i = 0; i < nextline.length(); i++)
			{
				//save the number stored in temp in value and push it to vector E
				if(nextline[i] == '|')
				{
					value = stoi(temp);
					E.push_back(value);
					temp = "";
					
				}
				else if(nextline[i] == '$')
				{
					//$ is end of line | clear temp
					temp = "";
				}	
				else
				{
					//add nextline[i] to temp
					temp += nextline[i];
				}
			}
		}		
		else if(line == "Current allocation matrix:")
		{
			while(nextline != "Request matrix:")
			{
				//get the nextline and save it in nextline and create empty vector row
				getline(input, nextline);
				vector<int> row;
				//go through nextline 
				for(int i = 0; i < nextline.length(); i++)
				{
					//save the number stored in temp in value and push it to vector row
					if(nextline[i] == '|')
					{
						value = stoi(temp);
						row.push_back(value);
						temp = "";
					}
					else if(nextline[i] == '$')
					{
						//$ is end of line | push vector row to the back of 2D vector C
						C.push_back(row);
					}	
					else
					{
						//add nextline[i] to temp
						temp += nextline[i];
					}
				}
			}
			temp = "";
			line = nextline;
		}
		else
		{
			nextline = line;
			while(nextline != "End of File")
			{
				//create empty vector row
				vector<int> rowe;
				for(int i = 0; i < nextline.length(); i++)
				{
					//save the number stored in temp in value and push it to vector row
					if(nextline[i] == '|')
					{
						value = stoi(temp);
						rowe.push_back(value);
						temp = "";
					}
					else if(nextline[i] == '$')
					{
						//$ is end of line | push vector row to the back of 2D vector R
						R.push_back(rowe);
					}	
					else
					{
						//add nextline[i] to temp
						temp += nextline[i];
					}
				}
				//get the nextline and save it in nextline
				getline(input, nextline);
			}
		}
	}
	
	//set all marks of the processes to false
	for(int i = 0; i < number_processes; i++)
	{
		marked[i] = false;
	}
	
	//create oftream object logger and open the file stored logfilename
	ofstream logger;
	logger.open(logfilename);
	logger << "Log of the Results" << endl;
	
	//set A to E and then A - C[i] to get the start value for vector A
	for(int j = 0; j < E.size(); j++)
	{
		A.push_back(E[j]);
		for(int i = 0; i < number_processes; i++)
		{
			A[j] -= C[i][j];
		}
	}
	
	//go trough the processes until agin is false
	while(again)
	{
		again = false;
		//go trough the processes
		for(int i = 0; i < number_processes; i++)
		{
			//execute when an unmarked process with R[i] <= A is found
			if((vector_comparison_less_or_equal(R[i], A)) && (!marked[i]))
			{
				//set rocess mark and agian to true
				marked[i] = true;
				again = true;
				for(int j = 0; j < C[i].size(); j++)
				{
					//add the values of vector C[i] to vector A
					A[j] += C[i][j];
					//set the values of vector C[i] and R[i] to 0
					C[i][j] = 0;
					R[i][j] = 0;
				}
				//save the index of the process and current A in the logfile
				logger << "Index of marked Process: " << i << endl;
				logger << "A: " << flush;
				for(int i = 0; i < A.size(); i++)
				{
					logger << A[i] << "|" << flush;
				}
				logger << endl;
			}
		}
	}	
	
	//get the processes involved in a deadlock if there are any
	for(int i = 0; i < number_processes; i++)
	{
		if(!marked[i])
		{
			logger << "Index of Process involved in Deadlock: " << i << endl;
		}
	}	
	
	//close input and logger
	input.close();
	logger.close();
}	