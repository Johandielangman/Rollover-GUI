# Rollover Application

*February 2025*

![demo](/img/demo.gif)

---

## ❓ Introduction

Welcome to the instructions for the Rollover Graphical User Interface! You’re probably wondering, “What is a rollover application?”

Let me paint a picture 🎨

You have two folders:

![project_folders.png](/img/project_folders.png)

Every year, you have to complete the same work using the same documents. It’s now 2025, and you need to use the templates from 2024 for the current year. So, you copy your 2024 report into the 2025 folder:

![copy_2024_to_2025.png](/img/copy_2024_to_2025.png)

You start working on `2025/report2024.xlsx`, but when you open the first sheet, you see this:

![what_is_this.png](/img/what_is_this.png)

What’s going on with this sheet? You’re not sure. But you remember that you had a reason for this. In fact, you wrote down the reason on one of the sheets you just deleted in the 2025 Excel file. Ah! But the sheet still exists in the old folder: `2024/report2024.xlsx`. So, you open last year’s Excel file.

But Excel doesn’t like this…

![excel_error.png](/img/excel_error.png)

Now you have two options:
1. Close the old Excel file every time you need to check a different year.
2. Rename each and every file.

But do you really want to rename all of these files?

![2024_input_files.png](/img/2024_input_files.png)

No way! No one has time for that! We’d much rather spend our valuable time doing something better… like making coffee ☕

This is where the Rollover application comes in!

## Demonstration

Let's open the application

![the_exe.png](/img/the_exe.png)

You will be greeted with the best application! *Rollover!*

![app_layout.png](/img/app_layout.png)

The application isn’t too complex, but let’s break down everything you can do and the feedback the app provides. I’ll walk you through an example shortly.  

1. This checkbox tells the application to look for occurrences of a year in your files and replace it with a different year. For example, if you have a file named `report 2024.xlsx`, the application will detect the year "2024" and replace it with the year you specify. In this case, we’ve selected 2025 in (2), so the file will become `report 2025.xlsx`. But what if the file name doesn’t contain a year? For instance, if your file is named `report.xlsx`, don’t worry! The application will add a suffix to the file, renaming it to `report (2025).xlsx`.  

2. This is the year to replace with. It’s a dropdown, and the default value is **2025**. You can select a year up to five years higher or lower.  

3. This checkbox enables or disables a custom suffix. Not every file needs or will have a year, so why not give users the option to add their own suffix? You can input your custom suffix in (4). You can also have both (1) and (3) enabled! The app will first add the year and then the custom suffix.  

4. This is where you enter the suffix to add to the end of your file name.  

5. This is the file browser. You can navigate your file system to select the folder the application should look at to rename the files. Keep in mind that the file browser will have a different look and feel from the one on your Windows laptop. I’ll provide some tips on how to use it later.  

6. Once you’ve selected your directory, you’ll see a preview here. This provides feedback on where the application is currently looking.  

7. This section shows all the files in the folder you selected in (5). You’ll see a checkbox next to each file. The application will rename only the files that are checked. By default, all Excel (xlsx) files will be selected, but you can toggle other files as well.  

8. This is similar to (5), but it shows where the renamed copy of the file will be saved. It’s important to note that the application will never rename a file if it results in a conflict. For example, if you want to rename `report 2024.xlsx` to `report 2025.xlsx`, but `report 2025.xlsx` already exists in the output folder, the app will not rename `report 2024.xlsx`.  

9. This is similar to (6), but for the output folder.  

10. This section displays all the files currently in the output directory. Once you click the rename button (13), your renamed files will appear here!  

11. This is a cool feature! We know there’s a lot going on, so we want to preview the changes the application is about to apply. When you toggle this checkbox, the application will show the changes in (7) with yellow text. It’s especially useful when you plan on doing complicated renames.  

12. This button resets everything. It removes all the inputs you’ve selected and allows you to start from scratch.  

13. Pressing this button will rename the files. If everything goes smoothly, the button will change from "Rename" to "Success". Once the files are renamed, you’ll need to press the "Reset" button to perform another rename.  

Let's give it a try

![file_browse.png](/img/file_browse.png)

In the above image:
1. Click on the Browse Files on the input side. This will open up the file browser. This doesn't look like the normal browser, I know. 
2. You can select a folder by clicking on it.
3. You should see the directory name at the bottom
4. Then press ok

A note. The application will always open the file browser from the location it's currently in. So, if you want to make it easier to select the file you want, you can move this application to the directory above the folder you want to select. This will make it easier to choose a file. 

You will also see that there is no back button. To go back, you double click on the two dots, to go into a directory, you double click on the name.

The application will then look like this:

![files_selected_preview.png](/img/files_selected_preview.png)

In the above image:
1. The application will show us the directory we selected. If it doesn't look right, we can try again.
2. We can see all the files in this directory. Note how the Excel (xlsx) files will have their checkbox automatically ticked. The application is built to solve the Excel problem after all!
3. But if we want to, we can always select the `foo.txt` file

Next, we select the output directory:

![output_file_browse.png](/img/output_file_browse.png)

In the above image:
1. Select the browse files
2. Select the output folder
3. Double check that we selected the correct folder
4. Click Ok.

We should see:

![click_the_preview.png](/img/click_the_preview.png)

In the above image:
1. We can double check that we selected the right directory
2. We can see what files are currently in this directory

So we have, by default, selected the option to change the year to `2025`. But what will this change look like? Click on the "Preview Changes" to see!

![preview_changes.png](/img/preview_changes.png)

In the above image:
1. We can see the changes the application is about to make to our files! For example, it wants to change `important_work_2024.xlsx` to `important_work_2025.xlsx`!
2. We can see that it also added the year to files where it couldn't find the year. For example, there is no year in `report1234.xlsx`. So instead, it wants to rename it to `report1234 (2025).xlsx`
3. Why isn't there a preview for `report2024.xlsx`? Well! This is because the proposed new name `report2025.xlsx` already exists in the output directory! The application doesn't want to overwrite your changes

But what if we want it to rename it? We can solve this by adding a custom suffix to every file:

![suffix.png](/img/suffix.png)

In the above image:
1. Enable the suffix option
2. Type in " demo" to the input
3. We will see the suffix applied to the preview.

Ok. I think we're ready to rename the files! Now we can click on the "Rename" button:

![renamed.png](/img/renamed.png)

In the above image:
1. As a visual feedback, the files in the input folder will be hidden and will suddenly appear in (2). This creates the illusion of the files moving over
2. We can see all our renamed files!
3. The application told us that it successfully renamed 7 files. This is also where other feedback messages will appear!
4. If we want to rename another set of files, we need to click on the reset button.


It worked! Don't believe me? Let's check the folder

![renamed_files.png](/img/renamed_files.png)

Ta-Da! 🎉 We have bulk renamed the files


## 📦 Download

You can click on the link below to download a zip file with:
1. The executable (which will be the application)
2. Instructions on how to use the application (this document)
3. A folder with a few documents to play around with
4. A demo video on how to see the tool in action

🔗 Download the package: [here](https://gelukkige-broodblik.s3.us-east-1.amazonaws.com/Rollover/rollover.zip)

## 📝 License

This project is [MIT](https://choosealicense.com/licenses/mit/) licensed.

---

Made with ❤️ by Johandielangman

[![BuyMeACoffee](https://img.shields.io/badge/Buy_Me_A_Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/johanlangman)