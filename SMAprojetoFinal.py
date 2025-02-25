from maspy import *
from maspy.learning import *
import numpy as np


class SortingBox(Environment):
    def __init__(self,env_name=None):
        super().__init__(env_name)
        self.create(Percept("Object_2000",("Shelf","Box_1","Box_2","Box_3","Box_0"),listed))
        self.create(Percept("Object_1500",("Shelf","Box_1","Box_2","Box_3","Box_0"),listed))
        self.create(Percept("Object_1507",("Shelf","Box_1","Box_2","Box_3","Box_0"),listed))
        self.create(Percept("Object_19",("Shelf","Box_1","Box_2","Box_3","Box_0"),listed))
        self.create(Percept("Object_105",("Shelf","Box_1","Box_2","Box_3","Box_0"),listed))
        self.possible_starts={"Object_2000":"Shelf","Object_1500":"Shelf","Object_1507":"Shelf","Object_19":"Shelf","Object_105":"Shelf"}

    def move_transition(self,state:dict,obj_to_box:tuple[str,str]):
        obj, box = obj_to_box
        obj_state:str = state[obj]
        if obj_state == "Shelf":
            state[obj] = box
            obj=self.is_divisible(obj.split("_")[-1])
            if(obj in ["Divisivel por 3,5,7"]):
                if box == "Box_1":
                    reward = -1
                if box == "Box_2":
                    reward = -2
                if box == "Box_3":
                    reward = 2   
                if box == "Box_0":
                    reward = -3   
            if(obj in ["Divisivel por 3,5","Divisivel por 3,7" ,"Divisivel por 5,7"]):
                if box == "Box_1":
                    reward = -1
                if box == "Box_2":
                    reward = 2
                if box == "Box_3":
                    reward =  -2
                if box == "Box_0":
                    reward = -3 
            if(obj in ["Divisivel por 5","Divisivel por 3","Divisivel por 7"]):
                if box == "Box_1":
                    reward = 2
                if box == "Box_2":
                    reward = -1
                if box == "Box_3":
                    reward = -2 
                if box == "Box_0":
                    reward = -3   
            if(obj in ["Não é divisivel por nenhum dos valores"]):
                if box == "Box_1":
                    reward = -1
                if box == "Box_2":
                    reward = -2
                if box == "Box_3":
                    reward = -3  
                if box == "Box_0":
                    reward = 2 

        else:
            reward = -2
        terminated = False
        for value in state.values():
            if value != "Shelf":
                continue
            break
        else:
            terminated = True
            
        return state,reward,terminated
    
    def is_divisible(self,obj):
        num = np.int64(obj)
        if(np.mod(num, 3) == 0 and np.mod(num, 5) == 0 and np.mod(num, 7) == 0):
            return "Divisivel por 3,5,7"
        elif(np.mod(num, 3) == 0 and np.mod(num, 5) == 0):
            return "Divisivel por 3,5"
        elif(np.mod(num, 3) == 0 and np.mod(num, 7) == 0):
             return "Divisivel por 3,7"
        elif(np.mod(num, 5) == 0 and np.mod(num, 7) == 0):
             return "Divisivel por 5,7"
        elif(np.mod(num, 5) == 0):
            return "Divisivel por 5"
        elif(np.mod(num, 3) == 0):
            return "Divisivel por 3"
        elif(np.mod(num, 7) == 0):
            return "Divisivel por 7"
        else:
            return "Não é divisivel por nenhum dos valores"



    #@action(listed,(('Object_1','Box_1'),('Object_1','Box_2'),('Object_1','Box_3'),('Object_2','Box_1'),('Object_2','Box_2'),('Object_2','Box_3')),move_transition)
    @action(cartesian,(('Object_2000','Object_1500','Object_1507','Object_19',"Object_105"),('Box_1','Box_2','Box_3','Box_0')),move_transition)
    def move(self,agt,obj_to_box:tuple[str,str]):
        obj,box=obj_to_box
        objeto= self.get(Percept(obj,Any))
        assert isinstance(objeto,Percept)
        self.print(f"{agt} is moving {obj} from {objeto.args} to {box}")
        self.change(objeto,box)




class BoxAgent(Agent):
    @pl(gain,Goal("make_model",Any))
    def makeModel(self,src,model_list:list[EnvModel]):
        model = model_list[0]
        print(f'actions:{model.action_space} space:{model.observation_space}')
        model.learn(qlearning,num_episodes=100)
        ag.auto_action = True
        ag.add_policy(model)







if __name__== "__main__":
    env = SortingBox()
    model = EnvModel(env)
    ag = BoxAgent()
    ag.add(Goal("make_model",[model]))
    Admin().start_system()

