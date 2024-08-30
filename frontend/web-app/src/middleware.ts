import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { cookies } from 'next/headers';
import { validateToken } from '@/app/lib/validation';

export async function middleware(req: NextRequest) {
    const path = req.nextUrl;

    if (path.pathname.startsWith('/home')) {
        const token = cookies().get('token')?.value;
        console.log(`Token: ${!token}`);

        if (!token) {
            console.log("No token in cookies, redirecting to login");
            return redirectToLogin(req);
        }

        const isValidToken = await validateToken(token);
        console.log(`Token is valid: ${isValidToken}`);
        if (!isValidToken) {
            console.log("Token is invalid, redirecting to login");
            const response = NextResponse.redirect(new URL('/login', req.url));
            response.cookies.delete('token');
            return response;
        }
    }

    if (path.pathname.startsWith('/login')) {
        const token = cookies().get('token')?.value;
        if (token) {
            console.log("Token found in cookies, redirecting to home");
            return redirectToHome(req);
        }
    }

    console.log(`Request path: ${path}`);
    return NextResponse.next();
}


function redirectToLogin(req: NextRequest) {
    const loginUrl = new URL('/login', req.url);
    return NextResponse.redirect(loginUrl);
}

function redirectToHome(req: NextRequest) {
    const homeUrl = new URL('/home', req.url);
    return NextResponse.redirect(homeUrl);
}