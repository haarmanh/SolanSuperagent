import Head from 'next/head';

export default function Custom404() {
  return (
    <>
      <Head>
        <title>404 - Page Not Found | Solān</title>
        <meta name="description" content="Page not found" />
      </Head>

      <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-md">
          <div className="text-center">
            <div className="w-16 h-16 bg-black text-white rounded-xl flex items-center justify-center font-bold text-2xl mx-auto mb-6">
              S
            </div>
            <h1 className="text-6xl font-bold text-gray-900 mb-4">404</h1>
            <h2 className="text-2xl font-semibold text-gray-700 mb-4">
              Page Not Found
            </h2>
            <p className="text-gray-600 mb-8">
              The page you're looking for doesn't exist or has been moved.
            </p>
            <div className="space-y-4">
              <a
                href="/"
                className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
              >
                Go Home
              </a>
              <div>
                <a
                  href="/dashboard"
                  className="text-blue-600 hover:text-blue-800 underline"
                >
                  Try Dashboard
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
