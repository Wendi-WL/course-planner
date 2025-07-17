import re

ops_pattern = re.compile(r"\([A-Za-z]\)")
and_period_pattern = re.compile(r"(?:\s[Aa][Nn][Dd]|\.)\s")

def split_dot_and(s):
    """Splits string into sections based on location(s) of 'and' and '.' within string (if any)
    
    String -> list of String
              or None if no splits needed"""

    diff = 0
    last_split = 0
    str = s
    subs = []
    prev = ops_pattern.search(str)
    split_spot = and_period_pattern.search(str)
    if split_spot is None:
        return None
    elif prev is not None:
        prev = prev.start()
        ops = True
    else:
        return and_period_pattern.split(s)

    while str:
        split_spot = and_period_pattern.search(str)
        op = ops_pattern.search(str)
        
        if split_spot is not None:
            sstart = split_spot.start()
            if op is None:
                period = re.search(r"\.\s", str)
                if period is not None:
                    subs += [s[last_split:period.start() + diff]]
                    last_split = period.end() + diff
                    str = str[period.end():]
                    diff += period.end()
                else:
                    if not subs:
                        return None
                    subs += [s[last_split:]]
                    break
            elif sstart < prev and sstart < op.start():
                subs += [s[last_split:sstart + diff]]
                last_split = split_spot.end() + diff
                str = str[split_spot.end():]
                diff += split_spot.end()
                prev -= diff
            else:
                str = str[op.end():]
                prev = 0
                diff += op.end()
        else:
            if not subs:
                return None
            subs += [s[last_split:]]
            break
        
    return subs


def split_ops(s):
    """Splits string into sections based on lettered options (ie (a), (b), etc)
    
    String -> Dictionary : {(a) : [list of String],
                            (b) : [list of String], 
                            ...}
                            
              or None if no sections"""
    
    idxs = ops_pattern.findall(s)
    if not idxs:
        return None
    all = ops_pattern.split(s)
    ops = [i for i in all if not re.fullmatch(r"\s?(?:\s|[Ee]ither|[Oo]ne [Oo]f|[Aa]ll [Oo]f)\s?", i)]

    options = {}
    for i in range(len(ops)):
        str = ops[i].strip()
        if str.endswith("or"):
            str = str[0:-3]
        options[idxs[i]] = str.strip(",.; ")
            
    return options

def req_dict(s):
    """Turns string of pre/coreqs into appropriately formatted dict of pre/coreqs
    
    String -> Dictionary : {"all of" : Dictionary or List of String,
                            "one of" : Dictionary or List of String,
                            "recommended" : Dictionary or List of String}
              or None if not able to parse
                            
    Assume string only contains requirement info"""

    reqs = {}

    def handle_str(s):
        # Assume string does not need to be split by 'and's or options
        s = s.strip(".,;[] ")
        course = re.fullmatch(r"([A-Z]{4})(?:_V)? ?([0-9]{3})", s)

        if re.search(r"recommend(?:ed)?", s, re.I) is not None:
            return {"recommended" : s}
        
        if re.match(r"one of ", s, re.I):
            l = re.split(r"(?:\sor|,)\s", s[6:])
            return {"one of" : handle_list(l, {})}
        
        if re.match(r"all of ", s, re.I):
            l = split_dot_and(s[6:])
            if l is not None:
                return handle_list(l, {})
            else:
                return {"all of" : handle_list(re.split(r"(?:\sand|,)\s", s[6:]), {})}
        
        if course is not None:
            return course[1] + " " + course[2]

        if re.match(r"[A-Z]{4}(?:_V)? ?[0-9]{3}", s):
            ors = s.find(" or ")
            course_matches = re.findall(r"([A-Z]{4})(?:_V)? ?([0-9]{3})", s)
            courses = [i[0] + " " + i[1] for i in course_matches]
            if ors >= 0:
                return {"one of" : courses}
            else:
                return {"all of" : courses}
        
        
        one = re.search(r"one of", s, re.I)
        all = re.search(r"all of", s, re.I)

        if one is not None:
            i = one.end()
            return {s[0:i] : handle_list(re.split(r"(?:\sor|,)\s", s[i:], re.I), {})}
        elif all is not None:
            i = all.span()
            return {s[0:i] : handle_list(re.split(r"(?:\sand|,)\s", s[i:], re.I), {})}
        else:
            return s
            
    def handle_list(l, dict):
        #print("\n")
        #print(l)
        #print(dict)
        li = []
        if not dict:
            ret_dict = False
        else:
            ret_dict = True

        for s in l:
            s = s.strip(".,[] ")
            d = handle_str(s)
            #print(d)
            if type(d) == dict:
                ret_dict = True
                for k, v in d.items():
                    add_to_dict(k, v, dict)
            else:
                li.append(d)
                add_to_dict("all of", d, dict)
        
        if ret_dict:
            #print("dict:")
            #print(dict)
            #print("(list:)")
            #print(li)
            return dict
        else:
            #print("list:")
            #print(li)
            #print("(dict:)")
            #print(dict)
            return li
    
    def add_to_dict(key, val, d):
        if type(val) == str:
            val = [val]
        if key == "one of" and key in d:
            i = 0
            while key in d:
                key = "one of " + str(i)
                i += 1

            d.update({key : val})
        elif key in d:
            if type(d[key]) == dict and type(val) == dict:
                d[key].update(val)
            else:
                d[key] += val
        else:
            d.update({key : val})
        return d

    def add_str(s):
        ops = split_ops(s)
        if ops is not None:
            for k, v in ops.items():
                ops[k] = handle_str(v)
                if type(ops[k]) == str:
                    ops[k] = [ops[k]]
            if re.match(r"\s?all of\s", s, re.I):
                add_to_dict("all of", ops, reqs)
            else:
                add_to_dict("one of", ops, reqs)
        else:
            req = handle_str(s)
            if type(req) == dict:
                for k, v in req.items():
                    add_to_dict(k, v, reqs)
            else:
                add_to_dict("all of", [req], reqs)

    parts = split_dot_and(s)
    if parts is not None:
        for part in parts:
            add_str(part)
    else:
        add_str(s)

    return reqs
