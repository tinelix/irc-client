#include "framework.h"
#include <windows.h>
#include <CommCtrl.h>
#include <stdio.h>
#include <wchar.h>
#include "resource.h"
#include "MainWindow.h"
#include "Globals.h"

LRESULT CALLBACK    WndProc(HWND, UINT, WPARAM, LPARAM);
INT_PTR CALLBACK    About(HWND, UINT, WPARAM, LPARAM);

WCHAR szTitle[256];                  // Текст строки заголовка
WCHAR szWindowClass[256];            // имя класса главного окна

MainWindow::MainWindow(HINSTANCE hInst)
{
    WNDCLASSEXW wcex = { 0 };

    wcex.cbSize = sizeof(WNDCLASSEX);

    wcex.style = CS_HREDRAW | CS_VREDRAW;
    wcex.lpfnWndProc = WndProcCallback;
    wcex.cbClsExtra = 0;
    wcex.cbWndExtra = 0;
    wcex.hInstance = hInst;
    wcex.hIcon = LoadIcon(hInst, MAKEINTRESOURCE(IDI_TINELIXIRC));
    wcex.hCursor = LoadCursor(nullptr, IDC_ARROW);
    wcex.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wcex.lpszMenuName = MAKEINTRESOURCEW(IDC_TINELIXIRC);
    wcex.lpszClassName = L"MainWindow";
    wcex.hIconSm = LoadIcon(wcex.hInstance, MAKEINTRESOURCE(IDI_SMALL));

    ::RegisterClassExW(&wcex);
}

MainWindow::~MainWindow()
{
    if (m_hwnd)
        DestroyWindow(m_hwnd);
}

HWND MainWindow::GetHwnd() {
    return m_hwnd;
}

HWND MainWindow::InitInstance(HINSTANCE hInstance, int nCmdShow)
{
    hInst = hInstance;

    HWND hWnd = CreateDialog(hInstance, MAKEINTRESOURCE(IDD_MAINWINDOW), NULL, NULL);

    if (hWnd)
    {
        HMENU hSysMenu = GetSystemMenu(hWnd, FALSE);
        InsertMenu(hSysMenu, 5, MF_BYPOSITION, IDM_ABOUT, TEXT("About..."));
        InsertMenu(hSysMenu, 5, MF_BYPOSITION | MF_SEPARATOR, 0, NULL);
        SetWindowText(hWnd, szWindowClass);
        HWND tabctrl = GetDlgItem(hWnd, IDC_THREADTABS);
        TCITEM tci = { 0 };
        tci.mask = TCIF_TEXT;
        tci.pszText = (LPWSTR)L"Thread";
        TabCtrl_InsertItem(tabctrl, 0, &tci);
        HMENU hMainMenu = LoadMenu(hInst, MAKEINTRESOURCE(IDC_TINELIXIRC));
        SetMenu(hWnd, hMainMenu);
    }
    else {
        MessageBox(hWnd, TEXT("Something wen\'t wrong..."), TEXT("Error"), MB_ICONERROR | MB_OK);
    }
    m_hwnd = hWnd;

    return hWnd;
}

LRESULT CALLBACK MainWindow::WndProcCallback(HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam)
{
    MainWindow* mainWnd;

    if (message == WM_CREATE)
    {
        CREATESTRUCT* cs = reinterpret_cast<CREATESTRUCT*>(lParam);
        mainWnd = static_cast<MainWindow*>(cs->lpCreateParams);
        mainWnd->m_hwnd = hwnd;
        ::SetWindowLongPtr(hwnd, GWLP_USERDATA, reinterpret_cast<LONG_PTR>(mainWnd));
    }
    else
        mainWnd = reinterpret_cast<MainWindow*>(::GetWindowLongPtr(hwnd, GWLP_USERDATA));

    if (mainWnd)
        return mainWnd->WndProc(message, wParam, lParam);

    return ::DefWindowProc(hwnd, message, wParam, lParam);
}

LRESULT CALLBACK MainWindow::WndProc(UINT message, WPARAM wParam, LPARAM lParam)
{
    switch (message)
    {
    case WM_CREATE:
    {
        HWND dummyWnd;
        RECT rect;

        dummyWnd = CreateWindowEx(0, TEXT("STATIC"), TEXT("STATIC"), 0, CW_USEDEFAULT, CW_USEDEFAULT, 0, 0, NULL, NULL,
            hInst, NULL);
        GetWindowRect(dummyWnd, &rect);
        DestroyWindow(dummyWnd);

        /* Move the dialog to where the dummy window was positioned */
        SetWindowPos(m_hwnd, 0, rect.left, rect.top, 0, 0, SWP_NOSIZE | SWP_NOZORDER);
        OutputDebugStringW(L"TEST! OnCreate\r\n");
        return 0;
    }
    break;
    case WM_COMMAND:
    {
        OutputDebugStringW(L"TEST! OnCommand\r\n");
        int wmId = LOWORD(wParam);
        // Разобрать выбор в меню:
        switch (wmId)
        {
        case IDM_ABOUT:
            DialogBox(hInst, MAKEINTRESOURCE(IDD_ABOUTBOX), m_hwnd, NULL);
            break;
        case IDM_EXIT:
            DestroyWindow(m_hwnd);
            break;
        default:
            return DefWindowProc(m_hwnd, message, wParam, lParam);
        }
    }
    break;
    case WM_PAINT:
    {
        PAINTSTRUCT ps;
        HDC hdc = BeginPaint(m_hwnd, &ps);
        OutputDebugStringW(L"TEST! OnPaint\r\n");
        EndPaint(m_hwnd, &ps);
    }
    break;
    case WM_DESTROY:
        PostQuitMessage(0);
        break;
    }

    char log[48];

    sprintf_s(log, "TEST! Message ID: %d\r\n", message);
    OutputDebugStringA(log);
    return DefWindowProc(m_hwnd, message, wParam, lParam);
}

LRESULT MainWindow::DefWndProc(UINT message, WPARAM wParam, LPARAM lParam)
{
    return ::DefWindowProc(m_hwnd, message, wParam, lParam);
}

// Обработчик сообщений для окна "О программе".
INT_PTR CALLBACK MainWindow::About(HWND hDlg, UINT message, WPARAM wParam, LPARAM lParam)
{
    UNREFERENCED_PARAMETER(lParam);
    switch (message)
    {
    case WM_INITDIALOG:
        return (INT_PTR)TRUE;

    case WM_COMMAND:
        if (LOWORD(wParam) == IDOK || LOWORD(wParam) == IDCANCEL)
        {
            EndDialog(hDlg, LOWORD(wParam));
            return (INT_PTR)TRUE;
        }
        break;
    }
    return (INT_PTR)FALSE;
}

bool MainWindow::ShowDialog() {
    if(m_hwnd) {
        ShowWindow(m_hwnd, SHOW_OPENWINDOW);
        return true;
    } else {
        return false;
    }
}