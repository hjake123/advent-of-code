class FileSystemNode:
    def __init__(self, name:str, size: int, superdir=None):
        self.subdirs = [] # List of subdirectories; empty for files.
        self.superdir = superdir
        self.name = name
        self.own_size = size

    def is_file(self) -> bool:
        '''
        Whether this node represents a file.
        '''
        return self.own_size > 0
    
    def get_size (self) -> int:
        '''
        Get the size of this node and all subnodes in the file system tree recursively.
        '''
        size = self.own_size
        for subdir in self.subdirs:
            size += subdir.get_size()
        return size
    
    def print(self, depth=0):
        '''
        Print yourself and your subdirectories.
        '''
        for i in range(0, depth):
            print('  ', end='')
        print(self.name, self.get_size())
        for subdir in self.subdirs:
            subdir.print(depth+1)
    
# The root of the File System tree.
top_directory = FileSystemNode('/', 0)

# A list of references to each directory for easy scanning later.
directory_list = [top_directory]

def find_named_subdir(name: str, current_directory: FileSystemNode):
    for subdir in current_directory.subdirs:
        if subdir.name == name:
            return subdir
    print("Undefined sub directory ", str)
    return current_directory

def read_cli_log(filename):
    with open(filename) as lines:
        for line in lines:
            state = 'OUTPUT'
            for token in line.split():
                if token == '$':
                    state = 'COMMAND'
                elif state == 'COMMAND' and token == 'cd':
                    state = 'CHDIR'
                elif state == 'COMMAND' and token == 'ls':
                    state = 'END' # Ignore ls commands.
            
            #Change Directory processing
                elif state == 'CHDIR' and token == '/':
                    current_directory = top_directory
                    state = 'END'
                elif state == 'CHDIR' and token == '..':
                    current_directory = current_directory.superdir
                    state = 'END'
                elif state == 'CHDIR':
                    current_directory = find_named_subdir(token, current_directory)
                    state = 'END'

            # CLI Output processing
                elif state == 'OUTPUT' and token == 'dir':
                    state = 'ADD_NODE'
                    node_size = 0
                elif state == 'OUTPUT':
                    state = 'ADD_NODE'
                    node_size = int(token)

                elif state == 'ADD_NODE':
                    node = FileSystemNode(token, node_size, current_directory)
                    directory_list.append(node)
                    current_directory.subdirs.append(node)  
                    state = 'END'

                else:
                    print("Token parsing error at ", token, " in line ", line)

read_cli_log("day7/in.txt")      
solution = 0
for directory in directory_list:
    if not directory.own_size == 0:
        continue
    size = directory.get_size()
    if size <= 100000:
        solution += size
print(solution)