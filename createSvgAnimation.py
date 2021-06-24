from bs4 import BeautifulSoup
from re import compile

def handler_from_file(filename):
    html = open(filename, 'r')
    return BeautifulSoup(html, 'xml')

def group(svgs):
    """The first svg is a base img. Adds additional svgs as animation tags

    Args:
        svgs ([[string, int]]): [[svg filename, length of animation]]
    """
    base = handler_from_file(svgs[0][0])
    tags = base.find_all('path')
    soups = [handler_from_file(name) for [name, dur] in svgs]
    durs = [svg[1] for svg in svgs]

    for tag in tags:

        id = tag.get('id')
        d = tag.get('d')


        if not id:
            continue

        matches = [x for x in [s.find('path', id=id) for s in soups] if x is not None]
        if (len(matches) == 0):
            continue
        ds = [mch.get('d') for mch in matches]
        if (len(set(ds + [d])) == 1):
            continue

        # print(f"ds: {len(ds)}, durs: {len(durs)}, range: {range(1,len(ds))} ")
        for cnt in range(1,len(ds)):
            animId = f"{id}-{str(cnt)}"
            animate = base.new_tag('animate', id=animId)
            animate.attrs['to'] = ds[cnt]
            animate.attrs['attributeName'] = 'd'
            animate.attrs['dur'] = f"{durs[cnt]}ms"
            animate.attrs['fill'] = "freeze"
            
            if cnt == 1:    #If this is the first animation layer
                animate.attrs['begin'] = f"0s;{id}-{str(len(ds) - 1)}.end" #start the animation at 0s, and the end of the last animation(loops)
            else:
                animate.attrs['begin'] = f"{id}-{str(cnt - 1)}.end"     #start the animation at the end of the previous animation
            tag.append(animate)
            
    return base

def write(output, svg):
    with open(output, "w") as file:
        file.write(str(svg))


svgs = [
    ["./trombone.svg", 1000],
    ["./trombone2.svg", 1000],
    ["./trombone3.svg", 1000],
    ["./trombone4.svg", 1000],
]
output="trombone-anim.svg"

animation = group(svgs)
write(output, animation)
