from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import camelot
import re
import os.path
import os


def add_content_weightage_in_data(data):
    for i in range(len(data)):

        # contain_weightage.append(data[i[1]]/data[i[2]])
        data[i].append(data[i][1]/data[i][2])
    return data


def print_data(data):
    for i in data:
        print(i)
    print()
    return data


def sort_data(data):
    for i in range(len(data)):
        for j in range(len(data)):
            # print(i[3])
            if data[i][2] > data[j][2]:
                temp = data[i]
                data[i] = data[j]
                data[j] = temp
    print()
    return data


def home(request):
    if request.method == 'POST' and request.FILES['pdf']:
        pdf = request.FILES['pdf']
        #print(os.getcwd(), '     nnnnn')
        # print(os.path.abspath(os.path.dirname(__file__)))
        path = os.getcwd()
        print(path, '           path')
        fs = FileSystemStorage()
        filename = fs.save(pdf.name, pdf)
        uploaded_file_url = fs.url(filename)
        file_path = path + '\\media\\' + pdf.name
        print(file_path)
        tables = camelot.read_pdf(file_path, pages='all',  strip_text=' .\n')

        ans = []  # all data are store in this

        # this loop use to strore value in ans
        for k in range(1, len(tables)-1):
            if k == 1:
                ind = 1
            else:
                ind = 0
            for i in range(ind, len(tables[k].df.index)):
                temp = []
                for j in range(len(tables[k].df.columns)):
                    temp.append(tables[k].df[j][i])
                ans.append(temp)

        # it modify the ans list
        for i in range(len(ans)):
            print(ans[i])
            if ans[i]:
                ans[i][1] = len(ans[i][1].split(','))
                if ans[i][3]:
                    ans[i][3] = int(re.search(r'\d+', ans[i][3]).group())
                if ans[i][0]:
                    ans[i][0] = int(re.search(r'\d+', ans[i][0]).group())
                else:
                    ans[i-1][1] += ans[i][1]
                    ans[i] = ''

        try:
            ans.remove('')
        except:
            pass
        for i in ans:
            i.remove(i[2])

        data = ans
        # 2. add content/weightage list in data
        add_content_weightage_in_data(data)

        print_data(data)

        # 3. sort 1. step list according to content/weightage list
        sort_data(data)

        print_data(data)
        final_ans = []
        count = 1
        for i in data:
            temp = {}
            temp['Priority_No'] = count
            temp['Unit_No'] = i[0]
            final_ans.append(temp)
            count += 1
        print(final_ans)
        return render(request, 'home.html', {'final_ans': final_ans, 'pdf_name': pdf.name[:-4]})
    return render(request, 'home.html', {'name': 'Nirmal'})
