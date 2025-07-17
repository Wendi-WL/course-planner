import re


def split_by_option(req):
    """Splits string into possible prereq 'paths' that can be taken
    String -> Dictionary
    
    If string starts with 'either' (case insensitive), finds and 
    splits string into dict where each key is the option's id 
    ((a), (b) etc) and each entry is the string that followed the
    id. If string does not start with 'either', return given str
    with id (a) for simplicity in turning into a model"""

    if re.match(r"(?:either|one of (a))", req, re.I):
        parts = re.split(r"\([a-z]\)", req[7:])
        parts.remove('')
        idxs = re.findall(r"\([a-z]\)", req)
        options = {}
        for i in range(len(parts)):
            str = parts[i]
            str = str.strip()
            if str.endswith("or"):
                str = str[0:-3]
            options[idxs[i]] = str
        return options
    else:
        return {"(a)" : req}


def req_dict(list):
    """Turns list of prereqs into an appropriately formatted dict of prereqs
    (listof String) -> Dictionary
    
    !!! NEED TO WRITE TESTS FOR THIS, only lightly tested so far"""


    requirements = {}

    def handle_str(s, key, requirements):
        """Turns single string into dict entry, adds entry to given dict
        String String Dict -> None"""


        s = s.strip(".,; ")
        rec = re.search(r"recommended", s, re.I)

        if re.match("one of", s, re.I):
            l = re.split(r"(?:\sor|,)\s", s[6:])
            list_to_dict(l, "one of", requirements)


        elif re.match(r"[A-Z]{4}(?:_V)? ?[0-9]{3}", s):
            
            if (s.find("or") > 0):
                key = "one of"
            elif rec is not None:
                key = "recommended"
            courses = re.findall(r"[A-Z]{4}(?:_V)? ?[0-9]{3}", s)
            if key in requirements:
                requirements[key] += courses
            else:
                requirements.update({key : courses})


        else:
            one = re.search(r"one of", s, re.I)
            all = re.search(r"all of", s, re.I)

            if one is not None:
                i = one.span()
                if rec is not None:
                    requirements["recommended"] = handle_list(re.split(r"(?:\sor\s|,)", s[i[1]:]))
                else:
                    requirements[s[0:i[1]]] = handle_list(re.split(r"(?:\sor\s|,)", s[i[1]:]))
            elif all is not None:
                i = all.span()
                if rec is not None:
                    requirements["recommended"] = handle_list(re.split(r",\s", s[i[1]:]))
                else:
                    requirements[s[0:i[1]]] = handle_list(re.split(r",\s", s[i[1]:]))
            elif s != "":
                if "all of" in requirements:
                    requirements["all of"].append(s)
                else:
                    requirements.update({"all of" : [s]})
        return


    def list_to_dict(l, key, requirements):
        """Applys handle_str to every entry in the given list
        (listof String) String Dictionary -> None"""

        for req in l:
            handle_str(req.strip(), key, requirements)
        return

    def handle_list(l):
        """Tidys every string in the list
        (listof String) -> (listof String)"""
        li = []
        for e in l:
            li.append(e.strip())
        return li


    list_to_dict(list, "all of", requirements)

    return requirements

def course_info(str):
    # Separate description from prereqs and coreqs
    cdf = re.search(r"This course is not eligible for Credit/D/Fail grading.", str)

    if cdf is not None:
        s = str[:cdf.start()] + str[cdf.end():]
    
    li = re.split(r"(?:[Rr]ecommended )?(?:[Pp]re|[Cc]o)-?requisite[s]:", s)
    sect = re.findall(r"(?:[Pp]re|[Cc]o)-?requisite:", s)
    equiv = re.search(r"equivalency:", str, re.I)
    
    desc = li[0].strip()
    prereq = None
    coreq = None

    if equiv is not None:
        desc += str[equiv.end():]
    if (cdf >= 0):
        desc += " This course is not eligible for Credit/D/Fail grading."
    
    if len(li) > 2:
        prereq = li[1].strip()
        coreq = li[2].strip()
    elif len(li) == 2 and re.match("pre", sect[0], re.I):
        prereq = li[1].strip()
        coreq = None
    elif len(li) == 2:
        prereq = None
        coreq = li[1].strip()
    else:
        prereq = None
        coreq = None

    return [desc, prereq, coreq]