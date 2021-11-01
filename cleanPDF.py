try:
    import PyPDF2 as pdf
except ModuleNotFoundError:
    print("This program requires the module PyPDF2.\nPlease confirm that PyPDF2 is installed properly")
    raise SystemExit


class cleanPDF:
    def __init__(self, fileIn, fileOut):
        self.inPDF = pdf.PdfFileReader(fileIn, 'rb')
        self.keepPages = self.__listPages()
        self.__create(fileOut)

    def __listPages(self):
        keepPages = self.inPDF.trailer["/Root"]["/PageLabels"]["/Nums"]
        keepPages = [i-1 for i in keepPages if isinstance(i, int)][1:]
        keepPages.append(self.inPDF.getNumPages()-1)
        return keepPages

    def __getBookmarks(self, outline, result=[], level=0):
        for obj in outline:
            if isinstance(obj, list):
                self.__getBookmarks(obj, result, level+1)
            else:
                bookmarkedPage = self.inPDF.getDestinationPageNumber(obj)
                for i in self.keepPages:
                    if i >= bookmarkedPage:
                        break
                result.append((i, obj.title, level))
        return result

    def __create(self, fileOut):
        outPDF = pdf.PdfFileWriter()
        bookmarks = self.__getBookmarks(self.inPDF.getOutlines())
        parent, last = [None], -1
        for pageNumber, x in enumerate(self.keepPages):
            outPDF.addPage(self.inPDF.getPage(x))
            while(bookmarks and x == bookmarks[0][0]):
                if last > bookmarks[0][2]:
                    k = last - bookmarks[0][2]
                    while(k >= 0):
                        parent.pop()
                        k -= 1
                elif last == bookmarks[0][2]:
                    parent.pop()
                parent.append(outPDF.addBookmark(bookmarks[0][1], pageNumber, parent[-1]))
                last = bookmarks[0][2]
                bookmarks.pop(0)
        try:
            with open(fileOut, 'wb') as file:
                outPDF.write(file)
                print("deDuplicated PDF saved as",fileOut)
                print("Kept {} pages out of {} pages".format(outPDF.getNumPages(),self.inPDF.getNumPages()))
        except PermissionError:
            print("The file is open in some other program or you don't have permission to create file.")


if __name__ == "__main__":
    try:
        pdfIN = input("Enter name of input the pdf : ")
        if(pdfIN[-4:].lower() != '.pdf'):
            pdfIN+='.pdf'
        pdfOut = input("Enter name of the output pdf (leave it blank for the default name '#{}') : ".format(pdfIN))
        if not pdfOut:
            pdfOut = '#'+pdfIN
        elif (pdfOut[-4:].lower() != '.pdf'):
            pdfOut+='.pdf'
        cleanPDF(pdfIN, pdfOut)
    except FileNotFoundError:
        print("Make sure that the file '{}' exist in the current directory".format(pdfIN))