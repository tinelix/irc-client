// Tinelix IRC.cpp : Определяет точку входа для приложения.
//

#include "framework.h"
#include "Tinelix IRC.h"
#include <windows.h>
#include <CommCtrl.h>
#include <wchar.h>
#include "MainWindow.h"
#include "Globals.h"
#include <uxtheme.h>

#define MAX_LOADSTRING 100

// Глобальные переменные:
HINSTANCE hInst;                                // текущий экземпляр

// Отправить объявления функций, включенных в этот модуль кода:
ATOM                MyRegisterClass(HINSTANCE hInstance);
HWND                InitInstance(HINSTANCE, int);

int APIENTRY wWinMain(_In_ HINSTANCE hInstance,
                     _In_opt_ HINSTANCE hPrevInstance,
                     _In_ LPWSTR    lpCmdLine,
                     _In_ int       nCmdShow)
{
    UNREFERENCED_PARAMETER(hPrevInstance);
    UNREFERENCED_PARAMETER(lpCmdLine);

    hInst = hInstance;

    HWND hWnd_dummy;
    HWND hWnd;

    // TODO: Разместите код здесь.

    // Инициализация глобальных строк
    LoadStringW(hInstance, IDS_APP_TITLE, szTitle, MAX_LOADSTRING);
    LoadStringW(hInstance, IDC_TINELIXIRC, szWindowClass, MAX_LOADSTRING);
    MainWindow* mainWnd = new MainWindow(hInstance);

    // Выполнить инициализацию приложения:
    hWnd = mainWnd->InitInstance(hInstance, nCmdShow);
    if (!(hWnd_dummy = hWnd)) {

    } else {
        mainWnd->ShowDialog();
    };

    HACCEL hAccelTable = LoadAccelerators(hInstance, MAKEINTRESOURCE(IDC_TINELIXIRC));

    MSG msg;

    // Цикл основного сообщения:
    while (GetMessage(&msg, NULL, 0, 0))
    {
        if (!TranslateAccelerator(msg.hwnd, hAccelTable, &msg))
        {
            TranslateMessage(&msg);
            DispatchMessage(&msg);
        }
    }

    return (int) msg.wParam;
}

