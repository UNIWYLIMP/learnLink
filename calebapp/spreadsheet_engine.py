import csv
import pandas as pd
import random
import time
import os


class SpreadSheetGenerator:
    def __init__(self):
        self.department = ""
        self.session = ""
        self.NOCs = 0
        self.semester = 0
        self.level = 0
        self.courses = []
        self.courses_files = []
        self.message = ""
        self.p = ""
        self.dataSheet = None
        self.sortedSpreadsheet = []
        self.tut = 0

    def generator(self, session, department, mode_of_entry, level, description, noc, courses, courses_files, data_set,
                  semester):
        self.department = department
        self.session = session
        self.level = int(level)
        if str(mode_of_entry) == "direct_entry":
            de = 100
            self.level -= de
        else:
            pass
        self.semester = semester
        self.NOCs = int(noc)
        self.courses = courses
        for x in self.courses:
            self.tut += x[1]

        slab = random.randint(100000, 99999999)
        directoryName = f"{str(self.level)} Level {str(self.department)} {str(self.session)} (ID_{str(slab)})"
        cwd = os.getcwd()
        path = os.path.join(cwd, "RESULTSET", directoryName)
        # os.path.join(BASE_DIR, 'media')
        print(path)
        if not os.path.exists(path):
            print("path does not exist")
            os.mkdir(f"./calebcommunity/media/RESULTSET/{directoryName}")

        else:
            print("print error po4")

        totalCourses = []
        p = 0
        for x in courses_files:
            rank_file = pd.read_excel(x, engine="openpyxl")
            stats = 0
            course_file = []
            shell = []
            for index, row in rank_file.iterrows():
                if stats == 0:
                    header = ["MATRIC", "NAME", "GRADE"]
                    course_file.append(header)
                    shell = [row['MATRIC'], row['NAME'], row['GRADE']]
                    stats += 1
                else:
                    shell = [row['MATRIC'], row['NAME'], row['GRADE']]
                course_file.append(shell)
            self.courses_files.append(course_file)
        print(self.courses_files)
        totalCourses = self.courses_files

        rex_file = pd.read_excel(data_set, engine="openpyxl")
        stats = 0
        course_file = []
        shell = []
        for index, row in rex_file.iterrows():
            if stats == 0:
                shell = ["MATRIC",	"NAME",	"MOE", "TUT", "TUP", "WGP",	"GPA", "CGPA"]
                course_file.append(shell)
                shell = [row['MATRIC'], row['NAME'], row['MOE'], int(row['TUT']), int(row['TUP']), int(row['WGP']),
                         float(row['GPA']), float(row['CGPA'])]
                stats += 1
            else:
                shell = [row['MATRIC'], row['NAME'], row['MOE'], int(row['TUT']), int(row['TUP']), int(row['WGP']),
                         float(row['GPA']), float(row['CGPA'])]
            course_file.append(shell)
        self.dataSheet = course_file

        checks = self.checker(self.dataSheet)

        if checks == "valid":
            print("SPREADSHEET required Columns are provided\n")
            time.sleep(0.6)
            pass
        else:
            print("\nError from SPREADSHEET Record__")
            print("program Terminated....")
            return 0

        spreadsheet_record_index = self.get_id_index(self.dataSheet)
        self.sortedSpreadsheet = self.sorting_engine(spreadsheet_record_index, self.dataSheet)
        print("\n\nVALUE 1\n\n")
        print(spreadsheet_record_index)
        print("\n\nVALUE 1A\n\n")
        print(self.sortedSpreadsheet)
        print("\n\nVALUE ENDED\n\n")

        for x in range(len(totalCourses)):
            checks = self.course_checker(totalCourses[x])
            if checks == "valid":
                print(f"\n{self.courses[x]} required Columns are provided.")
                time.sleep(0.6)
                pass
            else:
                print(f"\nError from {self.courses[x]} Record__")
                print("program Terminated....")
                return 0

        tempResultSheet, tempMissingResult, probationList, averageGPA, percentagePassed, datasheet = self.grader(
            self.sortedSpreadsheet, totalCourses, self.courses,
            spreadsheet_record_index, self.level, self.semester, self.NOCs)

        fields = ["MATRIC NO", "NAME", "MOE", "PTUT", "PTUP", "PWGP", "PGPA", "PCGPA"]
        for q in self.courses:
            fields.append(f"{q[0]} [GRADE({q[1]})]")
            fields.append(f"{q[0]} [SCORE({q[1]})]")
        fields.append("STUT")
        fields.append("STUP")
        fields.append("SWGP")
        fields.append("SGPA")
        fields.append("TUT")
        fields.append("TUP")
        fields.append("WGP")
        fields.append("CGPA")
        with open(f'./calebcommunity/media/RESULTSET/{directoryName}/Spreadsheet.csv', 'w') as f:
            write = csv.writer(f)
            write.writerow(fields)
            write.writerows(tempResultSheet)
        df_new = pd.read_csv(f'./calebcommunity/media/RESULTSET/{directoryName}/Spreadsheet.csv')

        GFG = pd.ExcelWriter(f'./calebcommunity/media/RESULTSET/{directoryName}/Spreadsheet.xlsx')
        df_new.to_excel(GFG, index=False)
        GFG.save()

        raw = ["matric", "name"]
        for x in range(len(self.courses)):
            raw.append("_")
        raw.append("_")
        with open(f'./calebcommunity/media/RESULTSET/{directoryName}/Missing Result List.csv', 'w') as f:
            write = csv.writer(f)

            write.writerow(raw)
            write.writerows(tempMissingResult)

        df_new = pd.read_csv(f'./calebcommunity/media/RESULTSET/{directoryName}/Missing Result List.csv')
        GFG = pd.ExcelWriter(f'./calebcommunity/media/RESULTSET/{directoryName}/Missing Result List.xlsx')
        df_new.to_excel(GFG, index=False)
        GFG.save()

        bow = ["MATRIC", "NAME", "CGPA"]
        with open(f'./calebcommunity/media/RESULTSET/{directoryName}/Probation List.csv', 'w') as f:
            write = csv.writer(f)

            write.writerow(bow)
            write.writerows(probationList)
        df_new = pd.read_csv(f'./calebcommunity/media/RESULTSET/{directoryName}/Probation List.csv')
        GFG = pd.ExcelWriter(f'./calebcommunity/media/RESULTSET/{directoryName}/Probation List.xlsx')
        df_new.to_excel(GFG, index=False)
        GFG.save()
        pow = ["MATRIC", "NAME", "MOE", "TUT", "TUP", "WGP", "GPA", "CGPA"]
        with open(f'./calebcommunity/media/RESULTSET/{directoryName}/datasheet.csv', 'w') as f:
            write = csv.writer(f)

            write.writerow(pow)
            write.writerows(datasheet)
        df_new = pd.read_csv(f'./calebcommunity/media/RESULTSET/{directoryName}/datasheet.csv')

        GFG = pd.ExcelWriter(f'./calebcommunity/media/RESULTSET/{directoryName}/datasheet.xlsx')
        df_new.to_excel(GFG, index=False)
        GFG.save()

        doc = open(f'./calebcommunity/media/RESULTSET/{directoryName}/info.txt', 'w')
        doc.write(
            f"AVERAGE GPA: {averageGPA}GPA.\nPERCENTAGE PASSED: {percentagePassed}%.\nNO OF STUDENTS ON PROBATION: {len(probationList)} student(s).\nNO OF STUDENTS WITH MISSING COURSES: {len(tempMissingResult)} student(s).")
        doc.close()

        print(f"\nAVERAGE GPA: {averageGPA}GPA")
        print(f"\nPERCENTAGE PASSED: {percentagePassed}%")
        print(f"\nNO OF STUDENTS ON PROBATION: {len(probationList)} student(s).")
        print(f"\nNO OF STUDENTS WITH MISSING COURSES: {len(tempMissingResult)} student(s).")
        print(f"\nData has been computed at {path} directory. \n Proceed to working space to get computation.")
        return directoryName

    def checker(self, record):
        document_status = {'matric': 0, 'name': 0, 'cgpa': 0, 'moe': 0, 'tut': 0, 'tup': 0, 'wgp': 0, 'gpa': 0}
        for x in record[0]:
            if 'matric' == str(x).lower():
                document_status['matric'] += 1

            elif 'name' == str(x).lower():
                document_status['name'] += 1

            elif 'cgpa' == str(x).lower():
                document_status['cgpa'] += 1

            elif 'gpa' == str(x).lower():
                document_status['gpa'] += 1

            elif 'moe' == str(x).lower():
                document_status['moe'] += 1

            elif 'tut' == str(x).lower():
                document_status['tut'] += 1

            elif 'tup' == str(x).lower():
                document_status['tup'] += 1

            elif 'wgp' == str(x).lower():
                document_status['wgp'] += 1
            else:
                pass
        print("checked reached")
        if document_status['matric'] == 1 and document_status['name'] == 1 and document_status['cgpa'] == 1 and \
                document_status['moe'] == 1 and document_status['tut'] == 1 and document_status['tup'] == 1 and \
                document_status['wgp'] == 1 and document_status['gpa'] == 1:
            self.message = "valid"
            print("\n_____All required required columns are provided...")
            return self.message

        elif document_status['matric'] == 0 or document_status['name'] == 0 or document_status['cgpa'] == 0 or \
                document_status['moe'] == 0 or document_status['tut'] == 0 or document_status['tup'] == 0 or \
                document_status['wgp'] == 0 or document_status['gpa'] == 0:
            print(
                '\nCheck your dataset correctly, one of the required column (Matric, NAME, CGPA, GPA, MODE OF ENTRY, TUT, TUP, OR WGP) is not provided in the data given. Please check your dataset and ensure it is updated correctly!')
            self.message = "invalid"
            return self.message

        elif document_status['matric'] > 1 or document_status['name'] > 1 or document_status['cgpa'] > 1 or \
                document_status['moe'] > 1 or document_status['tut'] > 1 or document_status['tup'] > 1 or \
                document_status['wgp'] > 1 or document_status['gpa'] > 1:
            print(
                '\nCheck your dataset correctly, one of this column (Matric, NAME, CGPA, GPA, MODE OF ENTRY, TUT, TUP, OR WGP) appears to have one or multiple duplicates')
            self.message = "invalid"
            return self.message

    def course_checker(self, record):
        document_status = {'matric': 0, 'name': 0, 'grade': 0}
        for x in record[0]:
            if 'matric' == str(x).lower():
                document_status['matric'] += 1

            elif 'name' == str(x).lower():
                document_status['name'] += 1

            elif 'grade' == str(x).lower():
                document_status['grade'] += 1

            else:
                pass

        if document_status['matric'] == 1 and document_status['name'] == 1 and document_status['grade'] == 1:
            self.message = "valid"
            print("_____All required required columns are provided...")
            return self.message

        elif document_status['matric'] == 0 or document_status['name'] == 0 or document_status['grade'] == 0:
            print(
                'Check your dataset correctly, one of the required column (Matric, Name, OR GRADE) is not provided in the data given. Please check your dataset and ensure it is updated correctly!')
            self.message = "invalid"
            return self.message

        elif document_status['matric'] > 1 or document_status['name'] > 1 or document_status['grade']:
            print(
                'Check your dataset correctly, one of this column (Matric, Name, OR GRADE) appears to have one or multiple duplicates')
            self.message = "invalid"
            return self.message

    def get_id_index(self, record):
        self.p = {'matric': record[0].index("MATRIC"), 'name': record[0].index("NAME"), 'cgpa': record[0].index("CGPA"),
                  'gpa': record[0].index("GPA"), 'moe': record[0].index("MOE"), 'tut': record[0].index("TUT"),
                  'tup': record[0].index("TUP"), 'wgp': record[0].index("WGP")}
        return self.p

    def get_id_course_index(self, record):
        self.p = {'matric': record[0].index("matric"), 'name': record[0].index("name"),
                  'grade': record[0].index("grade")}
        return self.p

    def sorting_engine(self, indexes, sheet):
        self.message = "Sorting Spreadsheet According to matric"
        oldList = []
        newListM = []
        newListX = []
        finalList = []
        for x in range(len(sheet)):
            if x > 0:
                newListM.append(int(str(sheet[x][indexes['matric']])[3:]))
                oldList.append(str(sheet[x][indexes['matric']]))
        newListM.sort()
        for y in newListM:
            for x in oldList:
                if str(y) == x[3:]:
                    newListX.append(x)
                else:
                    pass

        for n in newListX:
            for x in range(len(sheet)):
                if x > 0:
                    if n == str(sheet[x][indexes['matric']]):
                        finalList.append(sheet[x])
                else:
                    pass
        return finalList

    def grader(self, sheet, coursesheet, courseslist, index, level, semester, noc):
        self.message = ""
        tup = self.tut
        totalScore = 0
        supremeGrade = []
        missingList = []
        probationList = []
        datasheet = []
        casterX = 0
        casterY = 0
        caster = 0
        for x in courseslist:
            totalScore += x[1]
        ntd = 0
        p = 0
        for x in sheet:
            superGrade = []
            grade = []
            q = 0
            if p < noc:
                p += 1

            for y in coursesheet:
                crop = []
                for z in range(len(y)):
                    if z > 0:
                        if str(y[z][0]) == str(x[index['matric']]):
                            ntd = 1
                            print(str(y[z][0]) + "/" + str(x[index['matric']]))
                            insurrection = False
                            try:
                                v = float(y[z][2])
                                if str(v) == "nan":
                                    insurrection = True
                            except ValueError:
                                insurrection = True

                            if insurrection:
                                tup -= self.courses[p - 1][1]
                                crop.append("F")
                                crop.append(0)
                                crop.append(0)

                            elif 0 > float(y[z][2]) > 100:
                                crop.append("F")
                                crop.append(0)
                                crop.append(0)

                            elif 0 <= float(y[z][2]) < 40:
                                crop.append("F")
                                crop.append(float(y[z][2]))
                                crop.append(0)

                            elif 40 <= float(y[z][2]) < 45:
                                crop.append("E")
                                crop.append(float(y[z][2]))
                                unit = courseslist[q][1]
                                vnt = unit * 0.2
                                crop.append(vnt)

                            elif 45 <= float(y[z][2]) < 50:
                                crop.append("D")
                                crop.append(int(y[z][2]))
                                unit = courseslist[q][1]
                                vnt = unit * 0.4
                                crop.append(vnt)

                            elif 50 <= float(y[z][2]) < 60:
                                crop.append("C")
                                crop.append(float(y[z][2]))
                                unit = courseslist[q][1]
                                vnt = unit * 0.6
                                crop.append(vnt)

                            elif 60 <= float(y[z][2]) < 70:
                                crop.append("B")
                                crop.append(float(y[z][2]))
                                unit = courseslist[q][1]
                                vnt = unit * 0.8
                                crop.append(vnt)

                            elif 70 <= float(y[z][2]) <= 100:
                                crop.append("A")
                                crop.append(float(y[z][2]))
                                unit = courseslist[q][1]
                                vnt = unit * 1.0
                                crop.append(vnt)
                            print(crop)
                            grade.append(crop)
                if ntd == 0:
                    crop.append("F")
                    crop.append(0)
                    crop.append(0)
                    grade.append(crop)
                q += 1

            static = 0
            p = 0
            for c in grade:
                p += 1
                static += c[2]
            gpa = (static / totalScore) * 5
            meta = ((level / 100) * 2) - 2
            if semester == 1:
                meta += 0
            elif semester == 2:
                meta += 1
            else:
                meta += 0
            xCgpa = float(x[index['cgpa']])
            pCgpa = xCgpa * meta
            rCgpa = pCgpa + gpa
            meta += 1
            cgpa = rCgpa / meta
            print("\n\n\n point reached")
            superGrade.append(x[index['matric']])
            superGrade.append(x[index['name']])
            superGrade.append(x[index['moe']])
            superGrade.append(x[index['tut']])
            superGrade.append(x[index['tup']])
            superGrade.append(x[index['wgp']])
            superGrade.append(x[index['gpa']])
            superGrade.append(x[index['cgpa']])

            for i in grade:
                superGrade.append(i[0])
                superGrade.append(i[1])
            superGrade.append(self.tut)
            superGrade.append(tup)
            superGrade.append(round(tup * gpa))
            superGrade.append(float('%.2f' % gpa))
            superGrade.append(int(x[index['tut']]) + self.tut)
            superGrade.append(int(x[index['tup']]) + tup)
            superGrade.append(round(int(x[index['wgp']]) + (tup * gpa)))
            superGrade.append(float('%.2f' % cgpa))
            supremeGrade.append(superGrade)
            tup = self.tut
            minorMissing = []
            subMissingList = []
            metadataset = []
            past = 0
            metadataset.append(x[index['matric']])
            metadataset.append(x[index['name']])
            metadataset.append(x[index['moe']])
            metadataset.append(int(x[index['tut']]) + self.tut)
            metadataset.append(int(x[index['tup']]) + tup)
            metadataset.append(round(int(x[index['wgp']]) + (tup * gpa)))
            metadataset.append(float('%.2f' % gpa))
            metadataset.append(float('%.2f' % cgpa))
            datasheet.append(metadataset)

            for k in range(len(grade)):
                if grade[k][1] == 0:
                    minorMissing.append(courseslist[k][0])
                    past = 1
            if past == 1:
                subMissingList.append(x[index['matric']])
                subMissingList.append(x[index['name']])

                for v in minorMissing:
                    subMissingList.append(v)
                subMissingList.append(cgpa)
                missingList.append(subMissingList)

            newMinor = []
            if cgpa < 2.25:
                newMinor.append(x[index['matric']])
                newMinor.append(x[index['name']])
                newMinor.append(float('%.2f' % cgpa))
                probationList.append(newMinor)

            if gpa >= 2.25:
                casterY += 1
            caster += 1
            casterX += gpa
        averageGPA = float('%.2f' % (casterX / caster))
        percentagePassed = (casterY / caster) * 100
        return supremeGrade, missingList, probationList, averageGPA, percentagePassed, datasheet
