import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@hooks/useAuth';
import styles from './Home.module.scss';
import Spinner from '@components/common/Spinner/Spinner';
import Button from '@components/common/Button/Button';
import Hero from '@components/ui/Hero/Hero';
import SidePanel from '@components/ui/SidePanel/SidePanel';
import Icon from '@components/common/Icon/Icon';

function Home() {
  const { isAuthenticated, isLoggingOut } = useAuth();
  const navigate = useNavigate();

  // Utenti autenticati vanno direttamente alla dashboard
  useEffect(() => {
    if (!isLoggingOut && isAuthenticated) {
      navigate('/dashboard', { replace: true });
    }
  }, [isAuthenticated, isLoggingOut, navigate]);

  // Non mostrare la landing durante il redirect
  if (isLoggingOut || isAuthenticated) return <Spinner />;

  return (
    <Hero>
      <Hero.Left>
        <SidePanel heading="MacerHappen" subheading="Scegli come vuoi vivere Macerata">
          <SidePanel.Inner>
            <div className={styles.description}>
              <h2>La piattaforma per scoprire e vivere gli eventi a Macerata</h2>
              <p className={styles.lead}>
                Tutto quello che succede in città in un unico posto: concerti, aperitivi, mostre, serate universitarie e altro
                ancora. Trova e organizza le tue uscite in pochi minuti.
              </p>

              <ul className={styles.features}>
                <li>
                  <Icon name="map" size="sm" />
                  <p>
                    <strong>Scopri cosa succede:</strong> esplora la mappa o la lista degli eventi filtrando per data, zona e
                    categoria.
                  </p>
                </li>
                <li>
                  <Icon name="ticket" size="sm" />
                  <p>
                    <strong>Vedi i dettagli:</strong> prezzo, orari, location e tutte le info pratiche in un colpo d&apos;occhio.
                  </p>
                </li>
                <li>
                  <Icon name="heart" size="sm" />
                  <p>
                    <strong>Segna ciò che ti piace:</strong> salva gli eventi che ti interessano e organizza le tue serate in
                    pochi tap.
                  </p>
                </li>
              </ul>
            </div>
          </SidePanel.Inner>

          <SidePanel.Actions>
            <p className={styles.note}>Hai già un account?</p>
            <Button href="/login" color="secondary" size="md" width="content">
              Accedi
            </Button>
          </SidePanel.Actions>
        </SidePanel>
      </Hero.Left>

      <Hero.Right background="splash" />
    </Hero>
  );
}

export default Home;
