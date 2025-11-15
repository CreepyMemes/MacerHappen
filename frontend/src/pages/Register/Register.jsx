// src/pages/Register/Register.tsx

import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@hooks/useAuth';
import Hero from '@components/ui/Hero/Hero';
import SidePanel from '@components/ui/SidePanel/SidePanel';
import Card from '@components/common/Card/Card';
import Button from '@components/common/Button/Button';
import Icon from '@components/common/Icon/Icon';
import styles from './Register.module.scss';

function Register() {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (isAuthenticated) navigate('/dashboard', { replace: true });
  }, [isAuthenticated, navigate]);

  const goToParticipant = () => navigate('/register/participant');
  const goToOrganizer = () => navigate('/register/organizer');

  return (
    <Hero>
      {/* LATO SINISTRO – spiegazione dei ruoli */}
      <Hero.Left>
        <SidePanel heading="MacerHappen" subheading="Scegli come vuoi vivere Macerata">
          <SidePanel.Inner>
            <div className={styles.description}>
              <h2>Partecipante o Organizzatore, pensiamo noi a tutto</h2>
              <ul className={styles.features}>
                <li>
                  <Icon name="user" size="sm" />
                  <p>
                    <strong>Partecipante:</strong> scopri con uno swipe gli eventi di Macerata in linea con i tuoi interessi e il
                    tuo budget.
                  </p>
                </li>
                <li>
                  <Icon name="organizer" size="sm" />
                  <p>
                    <strong>Organizzatore:</strong> crea eventi a Macerata, raggiungi il pubblico giusto e gestisci tutto da un
                    unico posto.
                  </p>
                </li>
              </ul>
            </div>
          </SidePanel.Inner>
          <SidePanel.Actions>
            <p className={styles.note}>Hai già un account?</p>
            <Button
              href="/login"
              color="secondary"
              size="md"
              width="content" //
            >
              Accedi
            </Button>
          </SidePanel.Actions>
        </SidePanel>
      </Hero.Left>

      {/* LATO DESTRO – scelta tra partecipante / organizzatore */}
      <Hero.Right background="background">
        <Card className={styles.register}>
          <div className={styles['register-form']}>
            <h2 className={styles.label}>Registrati</h2>
            <p className={styles.subtitle}>Come vuoi registrarti?</p>

            <div className={styles['button-group']}>
              <Button
                type="button"
                size="md"
                color="primary"
                wide
                className={styles.registerBtn}
                onClick={goToParticipant} //
              >
                Registrati come Partecipante
              </Button>

              <Button
                type="button"
                size="md"
                color="secondary"
                wide
                className={styles.registerBtn}
                onClick={goToOrganizer} //
              >
                Registrati come Organizzatore
              </Button>
            </div>
          </div>
        </Card>
      </Hero.Right>
    </Hero>
  );
}

export default Register;
