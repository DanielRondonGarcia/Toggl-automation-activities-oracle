# escape=`

# Use the latest Windows Server Core 2022 image.
FROM python:3-windowsservercore

# Restore the default Windows shell for correct batch processing.
SHELL ["cmd", "/S", "/C"]

# Copy our Install script.
COPY Install.cmd C:\TEMP\

# Download collect.exe in case of an install failure.
ADD https://aka.ms/vscollect.exe C:\TEMP\collect.exe

# Use the latest release channel. For more control, specify the location of an internal layout.
ARG CHANNEL_URL=https://aka.ms/vs/17/release/channel
ADD ${CHANNEL_URL} C:\TEMP\VisualStudio.chman

RUN `
    # Download the Build Tools bootstrapper.
    curl -SL --output vs_buildtools.exe https://aka.ms/vs/17/release/vs_buildtools.exe `
    `
    # Install Build Tools with the Microsoft.VisualStudio.Workload.AzureBuildTools workload, excluding workloads and components with known issues.
    && (call C:\TEMP\Install.cmd vs_buildtools.exe --quiet --wait --norestart --nocache install `
        --installPath "%ProgramFiles(x86)%\Microsoft Visual Studio\2022\BuildTools" `
        --channelUri C:\TEMP\VisualStudio.chman `
        --installChannelUri C:\TEMP\VisualStudio.chman `
        --add Microsoft.VisualStudio.Workload.AzureBuildTools `
        --add Microsoft.VisualStudio.ComponentGroup.VC.Tools.142.x86.x64 `
        --add Microsoft.VisualStudio.Component.Windows10SDK.19041 `
        --add Microsoft.VisualStudio.Component.Windows10SDK `
        --add Microsoft.VisualStudio.Component.VC.CoreIde `
        --add Microsoft.VisualStudio.Component.VC.CMake.Project `
        --add Microsoft.VisualStudio.Component.VC.14.29.16.11.CLI.Support `
        --add Microsoft.VisualStudio.ComponentGroup.UWP.VC.v142') `
    `
    # Cleanup
    && del /q vs_buildtools.exe

WORKDIR C:/oracle

ADD https://download.oracle.com/otn_software/nt/instantclient/219000/instantclient-basiclite-windows.x64-21.9.0.0.0dbru.zip .

RUN powershell -Command Expand-Archive -Path instantclient-basiclite-windows.x64-21.9.0.0.0dbru.zip

# Copy just .dll to root python folder
RUN powershell -Command Copy-Item -Path C:\oracle\instantclient-basiclite-windows.x64-21.9.0.0.0dbru\instantclient_21_9\*.dll -Destination C:\Python

WORKDIR C:/time

COPY ./Src .

RUN mkdir logs

RUN python -m pip install --upgrade pip setuptools wheel

RUN pip install -r requirements.txt

WORKDIR C:/time

# Define the entry point for the Docker container.
# This entry point starts the developer command prompt and launches the PowerShell shell.
ENTRYPOINT ["C:\\Program Files (x86)\\Microsoft Visual Studio\\2022\\BuildTools\\Common7\\Tools\\VsDevCmd.bat", "&&", "powershell.exe", "-NoLogo", "-ExecutionPolicy", "Bypass"]