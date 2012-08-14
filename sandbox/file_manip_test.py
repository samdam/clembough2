"""
Just some test code biatch
"""
def func():
    try:
        with open('a_file.txt', 'r') as f:
            change = raw_input('Change?  ')
            print "print 000000000000000000000000000000000\n", f.read()
            if change == 0:
                print "print 111111111111111111111111111111111111\n", f.read()
                return f.read()
            else:
                f.write(change)
                return "print 2222222222222222222222222222222222222\n", f.read()
    except IOError as e:
        f = open('a_file.txt', 'w+')
        print f.read()
        f.write('brand new')
        string = f.read()
        return string

def silly():
    pass

def main():
    print func()
    print "DDDDDDDDDDDDDONE"

if __name__== "__main__":
    main()
