import json 
import pandas as pd 
import socket 

def handle_date(obj): 
    if isinstance(obj, pd.Timestamp): 
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)


id = 0
if __name__ == "__main__":  
    with open("../datasets/news_data.json") as f: 
        data = json.load(f)
        #for _ in range(id): 
         #   next(iter(list(data)))
        #records = []
        '''for line in list(data): 
            records.append(line)
            if len(records) == 2: 
                chunk = pd.DataFrame(records)
                print(chunk)
                for record in chunk.to_dict(orient='records'): 
                    serialize_data = json.dumps(record, default=handle_date).encode("utf-8")
                    print("Serialize")
                    print(serialize_data)
                    id += 1 
                records = []'''
        print(len(list(data)))






