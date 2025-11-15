import { Routes, Route } from 'react-router-dom';
import ProtectedRoute from './ProtectedRoute';
import RoleRedirect from './RoleRedirect';

import Layout from '@components/layout/Layout/Layout';

import Home from '@pages/Home/Home';
import Login from '@pages/Login/Login';
import Register from '@pages/Register/Register';
import RegisterParticipant from '@pages/RegisterParticipant/RegisterParticipant';
import RegisterOrganizer from '@pages/RegisterOrganizer/RegisterOrganizer';

import VerifyEmail from '@pages/VerifyEmail/VerifyEmail';
import RequestPasswordReset from '@pages/RequestPasswordReset/RequestPasswordReset';
import ConfirmPasswordReset from '@pages/ConfirmPasswordReset/ConfirmPasswordReset';
import NotFound from '@pages/NotFound/NotFound';

// import Dashboard from '@pages/Dashboard/Dashboard';
// import Settings from '@pages/Settings/Settings';

// import BarberServices from '@pages/barber/BarberServices/BarberServices';
// import BarberAppointments from '@pages/barber/BarberAppointments/BarberAppointments';
// import BarberAvailabilities from '@pages/barber/BarberAvailabilities/BarberAvailabilities';
// import BarberReviews from '@pages/barber/BarberReviews/BarberReviews';

// import ClientAppointments from '@pages/client/ClientAppointments/ClientAppointments';
// import ClientReviews from '@pages/client/ClientReviews/ClientReviews';
// import ClientBarbers from '@pages/client/ClientBarbers/ClientBarbers';

// Helper for cleaner protected route declaration
const protectedRoute = (element, role) => <ProtectedRoute role={role}>{element}</ProtectedRoute>;

function AppRoutes() {
  return (
    <Routes>
      <Route element={<Layout />}>
        {/* Public pages (no need to be authenticated) */}
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/register/participant" element={<RegisterParticipant />} />
        <Route path="/register/organizer" element={<RegisterOrganizer />} />
        <Route path="/verify/:uidb64/:token" element={<VerifyEmail />} />
        <Route path="/reset-password" element={<RequestPasswordReset />} />
        <Route path="/reset-password/:uidb64/:token" element={<ConfirmPasswordReset />} />

        {/* Shortcut redirects (from /:page to  /:role/:page) */}
        <Route path="dashboard" element={protectedRoute(<RoleRedirect />)} />
        <Route path="settings" element={protectedRoute(<RoleRedirect />)} />

        {/* Role based pages */}
        {/* <Route path=":role/dashboard" element={protectedRoute(<Dashboard />)} />
        <Route path=":role/settings" element={protectedRoute(<Settings />)} /> */}

        {/* Unique role protected pages */}

        {/* <Route path="barber/services" element={protectedRoute(<BarberServices />, 'BARBER')} />
        <Route path="barber/appointments" element={protectedRoute(<BarberAppointments />, 'BARBER')} />
        <Route path="barber/availabilities" element={protectedRoute(<BarberAvailabilities />, 'BARBER')} />
        <Route path="barber/reviews" element={protectedRoute(<BarberReviews />, 'BARBER')} />

        <Route path="client/appointments" element={protectedRoute(<ClientAppointments />, 'CLIENT')} />
        <Route path="client/reviews" element={protectedRoute(<ClientReviews />, 'CLIENT')} />
        <Route path="client/barbers" element={protectedRoute(<ClientBarbers />, 'CLIENT')} /> */}

        {/* 404 page (this must be last) */}
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}

export default AppRoutes;
