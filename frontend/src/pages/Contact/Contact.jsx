import "./Contact.css";

function Contact() {
  // const theme = useTheme();
  // const isSmallScreen = useMediaQuery(theme.breakpoints.down("sm"));

  return (
    <div className='Page'>
      <div className='title-desc'>
        <h1>Contact Us</h1>
        <p className='desc'>
          We'd love to answer any questions and hear any feedback you may have.
        </p>
      </div>
      <section className='main-contact'>
        <div className='form-container'></div>
      </section>
    </div>
  );
}
export default Contact;
