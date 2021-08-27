class Stack:

    def __init__(self):
        self.stack_data = []

    def isEmpty(self):
        '''
        checking the stack for emptiness. The method returns True or False
        '''
        lengt = len(self.stack_data)

        if lengt == 0:
            print(True)
            return True

        elif lengt > 0:
            print(False)
            return False

    def push(self, element):
        '''
        adds a new item to the top of the stack
        :param element: any element
        :return: None
        '''
        self.stack_data.append(element)

    def pop(self):
        '''
        removes the top element of the stack. The stack changes.
        :return: The top elements of the stack
        '''

        if len(self.stack_data) > 0:
            del_element = self.stack_data.pop()
            #print(del_element)
            return del_element

        else:
            print('stack empty')

    def peek(self):

        '''
        :return: The top elements of the stack, but does not remove it. Stack does not change
        '''

        if len(self.stack_data) > 0:
            last_element = self.stack_data[-1]
            print(last_element)
            return last_element

        else:
            print('stack empty')

    def size(self):

        '''
        :return: The number of objects
        '''

        #print(len(self.stack_data))
        return len(self.stack_data)

    # def check_brackets(self, brackets):
    #
    #     if len(brackets) % 2 == 0:
    #         #print(' great ')
    #         print(len(brackets))
    #         print(brackets[6])



        # else:
        #     print(' bad ')

class Brackets:

    def check(self, checking_brackets):
        '''
        Checking  brackerts collection
        :param checking_brackets: string
        :return: None
        '''
        st = Stack()

        if len(checking_brackets) % 2 == 0:
            for i in checking_brackets:
                st.push(i)

            amount_of_elements = st.size()  # under the hood print()

            element_check_list = []

            result = True
            for i in range(amount_of_elements):

                element = st.pop()

                if element == ')' or element == '}' or element == ']':
                    element_check_list.append(element)

                elif element == '(':

                    if element_check_list.pop() == ')':
                        continue
                    else:
                        result = False
                        break

                elif element == '{':
                    if element_check_list.pop() == '}':
                        continue
                    else:
                        result = False
                        break

                elif element == '[':
                    if element_check_list.pop() == ']':
                        continue
                    else:
                        result = False
                        break

            if result == False:
                print('Несбалансирована ')
            else:
                print('Сбалансирована ')

        else:
            print('Несбалансирована ')


# if __name__=='__main__':
    #stack = Stack()
    # stack.isEmpty()
    # stack.push(1111)
    # stack.push(2222)
    # stack.push(3333)
    # stack.pop()
    # stack.peek()
    # stack.size()

    # bracket = Brackets()
    # bracket.check('{{[(])]}}')
    # bracket.check('(((([{}]))))')
    # bracket.check('[([])((([[[]]])))]{()}')
    # bracket.check('{{[()]}}')
    # bracket.check('}{}')
    # bracket.check('[[{())}]')
    # bracket.check('(())(()){{}}[[}]')
    #



