import re



def markdown_post(body):
    #print(body)
    body=check_paragraph(body)
    body=check_heading(body) # # ## ### #### ##### ######
    body=check_bold_italic(body) # ***
    body=check_bold(body) # **
    body=check_italic(body) # *
    body=check_breakline(body)
    #print(body)
    return body
    
def reverse_markdown_post(body):
    #print(body)
    body=reverse_check_paragraph(body)
    body=reverse_check_heading(body)
    body=reverse_check_bold_italic(body)
    body=reverse_check_bold(body)
    body=reverse_check_italic(body)
    body=reverse_check_breakline(body)
    #print(body)
    return body    
    
    
def check_heading(body):
    #print(body)
    heading_search = re.search(r"#+\s.+", body)#working
    all_heading = re.findall(r"#+\s.+", body)#working
    #heading_search = re.search(r"#+\s.+", body)
    #all_heading = re.findall(r"#+\s.+", body)
    print(all_heading)
    if heading_search:
        print("YES! We have a match!")
        for i in range(0,len(all_heading)):
            heading=all_heading[i]
            print(all_heading[i])
            temp_heading=''.join(heading)
            print(len(temp_heading))
            count_heading=temp_heading.count('#')
            temp_heading=temp_heading.replace("# ","")
            temp_heading=temp_heading.replace("#","")
            #temp_heading=temp_heading.replace(" ","")
            if '\r' in temp_heading:
                temp_heading=temp_heading[0:len(temp_heading)-1]
            print(len(temp_heading))
            if count_heading==1:
                body=body.replace(heading,'<h1>'+temp_heading+'</h1>')
            elif count_heading==2:
                body=body.replace(heading,'<h2>'+temp_heading+'</h2>')
            elif count_heading==3:
                body=body.replace(heading,'<h3>'+temp_heading+'</h3>')
            elif count_heading==4:
                body=body.replace(heading,'<h4>'+temp_heading+'</h4>')
            elif count_heading==5:
                body=body.replace(heading,'<h5>'+temp_heading+'</h5>')
            elif count_heading==6:
                body=body.replace(heading,'<h6>'+temp_heading+'</h6>')
            
    else:        
        print('noooo')
        print(all_heading,'huh')
    return body

def reverse_check_heading(body):
    #print(body)
    heading_search = re.search(r"<h\d>.+<\/h\d>", body)#working
    all_heading = re.findall(r"<h\d>.+<\/h\d>", body)#working
    #print(all_heading)
    if heading_search:
        print("YES! We have a match!")
        for i in range(0,len(all_heading)):
            heading=all_heading[i]
            print(all_heading[i])
            temp_heading=''.join(heading)
            print(len(temp_heading))
            if '\r' in temp_heading:
                temp_heading=temp_heading[0:len(temp_heading)-1]
                
            if '<h1>' in all_heading[i]:
                temp_heading=temp_heading.replace('<h1>',"")
                temp_heading=temp_heading.replace('</h1>',"")
                hashtags=1*'#'
                body=body.replace(heading,hashtags+' '+temp_heading)
            elif '<h2>' in all_heading[i]:
                temp_heading=temp_heading.replace('<h2>',"")
                temp_heading=temp_heading.replace('</h2>',"")
                hashtags=2*'#'
                body=body.replace(heading,hashtags+' '+temp_heading)
            elif '<h3>' in all_heading[i]:
                temp_heading=temp_heading.replace('<h3>',"")
                temp_heading=temp_heading.replace('</h3>',"")
                hashtags=3*'#'
                body=body.replace(heading,hashtags+' '+temp_heading)
            elif '<h4>' in all_heading[i]:
                temp_heading=temp_heading.replace('<h4>',"")
                temp_heading=temp_heading.replace('</h4>',"")
                hashtags=4*'#'
                body=body.replace(heading,hashtags+' '+temp_heading)
            elif '<h5>' in all_heading[i]:
                temp_heading=temp_heading.replace('<h5>',"")
                temp_heading=temp_heading.replace('</h5>',"")
                hashtags=5*'#'
                body=body.replace(heading,hashtags+' '+temp_heading)
            elif '<h6>' in all_heading[i]:
                temp_heading=temp_heading.replace('<h6>',"")
                temp_heading=temp_heading.replace('</h6>',"")
                hashtags=6*'#'
                body=body.replace(heading,hashtags+' '+temp_heading)
            print(body)
            
    else:        
        print('noooo')
        print(all_heading,'huh2')
    return body


def check_bold(body):
    print(body)
    #heading_search = re.search("(.*)(\*\*)(.+)(\*\*)(.*)", body)#working
    #all_heading = re.findall(r"(.*)\*\*(.+)\*\*(.*)", body)#working
    #heading_search = re.search("(\*\*)(.+)(\*\*)", body)#working
    #all_heading = re.findall(r"\*\*.+\*\*", body)#working
    heading_search = re.search("(\*\*)(\w+\s*\w*)(\*\*)", body)
    all_heading = re.findall(r"(\*\*)(\w+\s*\w*)(\*\*)", body)
    #print(all_heading)
    if heading_search:
        print("YES! We have a match!")
        for heading in all_heading:
            str_heading=''.join(heading)
            print(heading,0)
            print(heading_search.group(1),9)
            body=body.replace(str_heading,'<strong>'+heading[1]+'</strong>')

            
    else:        
        print('noooo')
        print(all_heading,'huh')
    return body

def reverse_check_bold(body):
    #print(body)
    heading_search = re.search(r"(<strong>)(\w+\s*\w*)(<\/strong>)", body)#working
    all_heading = re.findall(r"(<strong>)(\w+\s*\w*)(<\/strong>)", body)#working
    #print(all_heading)
    if heading_search:
        print("YES! We have a match!")
        for heading in all_heading:
            str_heading=''.join(heading)
            body=body.replace(str_heading,'**'+heading[1]+'**')

            
    else:        
        print('noooo')
        print(all_heading,'huh')
    return body    
    
def check_italic(body):
    #print(body)
    heading_search = re.search("(\*)(\w+\s*\w*)(\*)", body)
    all_heading = re.findall(r"(\*)(\w+\s*\w*)(\*)", body)
    #print(all_heading)
    if heading_search:
        print("YES! We have a match!")
        for heading in all_heading:
            str_heading=''.join(heading)
            #print(heading,0)
            #print(heading_search.group(1),9)
            body=body.replace(str_heading,'<em>'+heading[1]+'</em>')

            
    else:        
        print('noooo')
        print(all_heading,'huh')
    return body

def reverse_check_italic(body):
    #print(body)
    heading_search = re.search(r"(<em>)(\w+\s*\w*)(<\/em>)", body)#working
    all_heading = re.findall(r"(<em>)(\w+\s*\w*)(<\/em>)", body)#working
    #print(all_heading)
    if heading_search:
        print("YES! We have a match!")
        for heading in all_heading:
            str_heading=''.join(heading)
            body=body.replace(str_heading,'*'+heading[1]+'*')

            
    else:        
        print('noooo')
        print(all_heading,'huh')
    return body


def check_bold_italic(body):
    #print(body)
    heading_search = re.search("(\*\*\*)(\w+\s*\w*)(\*\*\*)", body)
    all_heading = re.findall(r"(\*\*\*)(\w+\s*\w*)(\*\*\*)", body)
    #print(all_heading)
    if heading_search:
        print("YES! We have a match!")
        for heading in all_heading:
            str_heading=''.join(heading)
            #print(heading,0)
            #print(heading_search.group(1),9)
            body=body.replace(str_heading,'<em>'+'<strong>'+heading[1]+'</strong>'+'</em>')

            
    else:        
        print('noooo')
        print(all_heading,'huh4')
    return body

def reverse_check_bold_italic(body):
    #print(body)
    heading_search = re.search(r"(<em>)(<strong>)(\w+\s*\w*)(<\/strong>)(<\/em>)", body)#working
    all_heading = re.findall(r"(<em>)(<strong>)(\w+\s*\w*)(<\/strong>)(<\/em>)", body)#working
    #print(all_heading)
    if heading_search:
        print("YES! We have a match!")
        for heading in all_heading:
            str_heading=''.join(heading)
            #print(str_heading,'bold_italic')
            body=body.replace(str_heading,'***'+heading[2]+'***')

            
    else:        
        print('noooo')
        print(all_heading,'huh5')
    return body    
    
    

def check_breakline(body):
    #print(body)
    heading_search = re.search(r"(.*)(\\)", body)
    all_heading = re.findall(r"(.*)(\\)", body)
    #print(all_heading)
    if heading_search:
        print("YES! We have a match!")
        for heading in all_heading:
            str_heading=''.join(heading)
            slash=heading[1]
            body=body.replace(slash,'</br>')

            
    else:        
        print('noooo')
        print(all_heading,'huh4')
    return body

def reverse_check_breakline(body):
    #print(body)
    heading_search = re.search(r"<\/br>", body)#working
    all_heading = re.findall(r"<\/br>", body)#working
    #print(all_heading)
    if heading_search:
        print("YES! We have a match!")
        for heading in all_heading:
            body=body.replace(heading,'\\')

            
    else:        
        print('noooo')
        print(all_heading,'huh5')
    return body    
    

def check_paragraph_2(body):
    print(body)
    print(repr(body))
    #heading_search = re.search(r"([\s\S]*)(\r)(\n)(\r)(\n)", body)#working #\r\n\r\n
    #all_heading = re.findall(r"([\s\S]*)(\r)(\n)(\r)(\n)", body)#working
    #print(re.sub("#+ h.+\r\n", "", body))
    #print(all_heading)
    if heading_search:
        print("YES! We have a match paragraph!")
        for heading in all_heading:
            str_heading=''.join(heading)
            str_heading=re.sub("#+ h.+\r\n", "", str_heading)
            str_heading=str_heading.split('\r\n\r\n')
            paragraph=re.sub("#+ h.+\r\n", "", heading[0])
            for head in str_heading:
                print(head,'head')
                paragraph=re.sub("#+ h.+\r\n", "", head)
                body=body.replace(head,'<p>'+head+'</p>')

            
    else:        
        print('noooo')
        print(all_heading,'huh6_0')
    return body
    
def check_paragraph(body):
    print(body)
    print(repr(body))
    heading_search = re.search(r"([\s\S]*)(\r)(\n)(\r)(\n)", body)#working #\r\n\r\n
    all_heading = re.findall(r"([\s\S]*)(\r)(\n)(\r)(\n)", body)#working
    #heading_search = heading_search.split('\r\n\r\n') 
    #print(re.sub("#+ h.+\r\n", "", body))
    #print(all_heading)
    if heading_search:
        print("YES! We have a match paragraph!")
        for heading in all_heading:
            str_heading=''.join(heading)
            str_heading=re.sub("#+ h.+\r\n", "", str_heading)
            paragraph=re.sub("#+ h.+\r\n", "", heading[0])
            body=body.replace(str_heading,'<p>'+paragraph+'</p>')

            
    else:        
        print('noooo')
        print(all_heading,'huh6_0')
    return body
    

def reverse_check_paragraph(body):
    print(body)
    heading_search = re.search(r"(<p>)([\s\S]*)(</p>)", body)#working
    all_heading = re.findall(r"(<p>)([\s\S]*)(</p>)", body)#working
    print(all_heading)
    if heading_search:
        print("YES! We have a match paragraph!")
        for heading in all_heading:
            str_heading=''.join(heading)
            print(str_heading,'bold_italic')
            body=body.replace(str_heading,heading[1]+'\r'+'\n''\r'+'\n')

            
    else:        
        print('noooo')
        print(all_heading,'huh6_1')
    return body        
# hi
#**yes wanker** yeah    
#**yeah** so what **I** like **it**

#please!

#https://stackoverflow.com/questions/35253694/html-tags-inside-paragraph-p
#https://stackoverflow.com/questions/2912894/how-to-match-any-character-in-regular-expression