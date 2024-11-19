#!/usr/bin/env python
import shutil, argparse, re, yaml
import lxml.etree as ET

with open('examples.yaml', encoding='utf-8') as stream:
    example_yaml = yaml.safe_load(stream)

for example in example_yaml["examples"]:

    # get the FILENAME
    try:
       exampleFileName = example["filename"]
    except:
       print("error in examples.yaml, no *filename* specified for entry")
       continue

    # get the DESCRIPTION
    try:
       exampleDescription = example["description"]
    except:
       print("error in examples.yaml, no *description* specified for entry")
       continue
    
    # get the CSS
    try:
       exampleCSS = example["CSS"]
    except:
       exampleCSS = ''

    # copy template to example file
    shutil.copyfile("../a11y-slides-math-template.html",exampleFileName)
    
    # read in the example file
    with open(exampleFileName, 'r') as file:
      filedata = file.read()
    
    # remove version number
    filedata = re.sub(r"#\s+V[0-9]+\.[0-9]+.*$",'# '+exampleDescription,filedata,flags=(re.MULTILINE))
    
    #......................
    #
    # <script>...</script> tags temporarily removed
    #
    #......................
    
    script_tag_count = 0
    script_tag_store = {}
    script_tag_match = re.match(r".*?(<script.*?<\/script>)",filedata,flags = (re.IGNORECASE | re.DOTALL))
    
    while script_tag_match:
          script_tag_store["script_tag_token"+str(script_tag_count)] = script_tag_match.groups(0)[0]
          filedata = re.sub(r"""<script
                                ((?:(?!<script).)*?)
                                <\/script>""",
                            "script_tag_token"+str(script_tag_count),filedata, 1, flags = (re.DOTALL|re.VERBOSE))
          script_tag_match = re.match(r".*?(<script.*?<\/script>)",filedata,flags = (re.IGNORECASE | re.DOTALL))
          script_tag_count += 1
    
    #......................
    #
    # HTML/CSS work
    #
    #......................
    # write the file out again
    with open(exampleFileName, 'w') as file:
      file.write(filedata)
    
    # now read as an XML tree
    tree = ET.parse(exampleFileName)
    
    tree.find('style').text += exampleCSS 
    
    # possibly update slides
    if "slides" in example:

       # empty the slides
       slideshowContainer = tree.find('.//div[@id="slideshow-container"]')
       for child in slideshowContainer:
           slideshowContainer.remove(child)

       # add new slides
       for slide in example["slides"]:
           newSlide = ET.Element('div')
           newSlide.attrib["class"] ="slide"
           for indv_element in slide["elements"]:
               attrib = {}

               # if there's any attributes...
               if 'attrib' in indv_element:
                   attrib = indv_element.pop('attrib')

               # create the <elements>
               for key in indv_element:
                   newElement = ET.Element(key)
                   newElement.text = indv_element[key]

                   # add attributes, if appropriate
                   for indv_attrib in attrib:
                       newElement.attrib[indv_attrib] = attrib[indv_attrib] 

                   newSlide.append(newElement)
           slideshowContainer.append(newSlide)

    # beautify the HTML
    ET.indent(tree,space='  ', level=0)

    # write HTML back to file
    tree.write(exampleFileName, pretty_print=True)
    
    #......................
    #
    # <script>...</script> tags back in
    #
    #......................
    
    # read in the example file
    with open(exampleFileName, 'r') as file:
      filedata = file.read()
    
    # now put the <script>...</script> tags back in
    for indv_script in script_tag_store:
        filedata = filedata.replace(indv_script, script_tag_store[indv_script])
    
    #......................
    #
    # replacments
    #
    #......................
    if "replacements" in example:
       for replacement in example["replacements"]: 
           if 'this' not in replacement:
              continue
           if 'that' not in replacement:
              replacement['that'] = ''
           filedata = filedata.replace(replacement["this"],replacement["that"])
    
    # write the file out again
    with open(exampleFileName, 'w') as file:
      file.write(filedata)
