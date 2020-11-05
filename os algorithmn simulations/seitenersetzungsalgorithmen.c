#include <stdio.h>
#include <stdlib.h>
typedef int bool;
#define true 1
#define false 0
#define empty_int -1
void init_arrays(int RAM[], int timer[], bool rbits[], int rahmen)
{
	for(int i = 0; i < rahmen; i++)
	{
		RAM[i] = empty_int;
	}
	
	for(int i = 0; i < rahmen; i++)
	{
		timer[i] = 1;
	}
	
	for(int i = 0; i < rahmen; i++)
	{
		rbits[i] = false;
	}
}

int max_magic(int timer[], bool rbits[], int rahmen)
{
	int temp = 0, imax;
	int temparray[rahmen];
	
	for(int i = 0; i < rahmen; i++)
	{
		temparray[i] = timer[i];
	}	
	
	for(int i = 0; i < rahmen; i++)
	{
		if(rbits[i] == true)
		{
			temparray[i] = 0;
		}
	}
	
	for(int i = 0; i < rahmen; i++)
	{
		if(temparray[i] > temp)
		{
			temp = temparray[i];
			imax = i;
		}
	}
	return imax;
}

int max_normal(int timer[], int rahmen)
{
	int temp = 0, imax;
	
	for(int i = 0; i < rahmen; i++)
	{
		if(timer[i] > temp)
		{
			temp = timer[i];
			imax = i;
		}
	}
	return imax;
}	


int main(int argc,char *argv[])
{
	int rahmen = 0, max_index = 0, max_index_normal = 0, j = 0, g = 0, num_elements = 0;
	int folge[] = {2,3,2,1,5,2,4,5,3,2,5,2}, timer[rahmen], RAM[rahmen];
	bool rbits[rahmen];
	
	sscanf (argv[1],"%d",&rahmen);
	
	init_arrays(RAM, timer, rbits, rahmen);
	
	printf("RAM Simulation 1.0\n");
	printf("--------------------------\n");
	printf("\n");
	
	while(1)
	{
		for(int i = 0; i < rahmen; i++)
		{
			if(folge[g] == RAM[i])
			{
				rbits[i] = true;
				goto print_jump;
			}
		}
		
		if(num_elements == rahmen)
		{
			max_index = max_magic(timer, rbits, rahmen);
			max_index_normal = max_normal(timer, rahmen);
			RAM[max_index] = folge[g];
			timer[max_index] = 0;
			rbits[max_index_normal] = false;
		}
		else
		{
			RAM[j] = folge[g];
			rbits[j] = false;
			num_elements++;
		}
		
		j++;
		print_jump: g++;
		
		for(int i = 0; i < num_elements; i++)
		{
			timer[i]++;
		}
		
		for(int i = 0; i < rahmen; i++)
		{
			printf("Page %d: %d rbit: %d Timer: %d\n", i, RAM[i], rbits[i], timer[i]);
		}
		
		printf("\n");
		
		if(g == sizeof(folge) / sizeof(int))
		{
			break;
		}
	}
	printf("--------------------------\n");
	printf("Exit Simulation...\n");
	return 0;
}	